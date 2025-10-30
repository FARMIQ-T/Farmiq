import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const CREDIT_AI_URL = Deno.env.get('CREDIT_AI_URL') || 'http://localhost:8000'
const supabase = createClient(
  Deno.env.get('SUPABASE_URL') ?? '',
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
)

interface USSDRequest {
  sessionId: string
  phoneNumber: string
  text: string
  serviceCode: string
}

interface MenuState {
  step: string
  farmerData?: any
  loanRequest?: any
}

async function getFarmerProfile(phoneNumber: string) {
  const { data, error } = await supabase
    .from('farmers')
    .select(`
      *,
      farm_details (*)
    `)
    .eq('phone_number', phoneNumber)
    .single()
  
  if (error) throw error
  return data
}

async function checkCreditScore(farmerData: any) {
  const response = await fetch(`${CREDIT_AI_URL}/predict/credit-score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      farm_size_acres: farmerData.farm_details.farm_size_acres,
      years_farming: farmerData.years_farming,
      crop_diversity: farmerData.farm_details.crop_diversity,
      yield_kg_per_acre: farmerData.farm_details.yield_kg_per_acre,
      yield_consistency: farmerData.farm_details.yield_consistency,
      monthly_revenue: farmerData.farm_details.monthly_revenue,
      expense_ratio: farmerData.farm_details.expense_ratio,
      existing_loans: 0, // Get from loans table
      repayment_history: 1.0, // Calculate from loan_payments
      training_hours: farmerData.farm_details.training_hours,
      coop_membership_years: farmerData.farm_details.coop_membership_years,
      advisory_visits: farmerData.farm_details.advisory_visits
    })
  })
  
  return await response.json()
}

async function simulateLoan(farmerData: any, loanAmount: number, termMonths: number) {
  const response = await fetch(`${CREDIT_AI_URL}/simulate/loan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      farmer: {
        // Same farmer data as above
        farm_size_acres: farmerData.farm_details.farm_size_acres,
        years_farming: farmerData.years_farming,
        crop_diversity: farmerData.farm_details.crop_diversity,
        yield_kg_per_acre: farmerData.farm_details.yield_kg_per_acre,
        yield_consistency: farmerData.farm_details.yield_consistency,
        monthly_revenue: farmerData.farm_details.monthly_revenue,
        expense_ratio: farmerData.farm_details.expense_ratio,
        existing_loans: 0,
        repayment_history: 1.0,
        training_hours: farmerData.farm_details.training_hours,
        coop_membership_years: farmerData.farm_details.coop_membership_years,
        advisory_visits: farmerData.farm_details.advisory_visits
      },
      loan_amount: loanAmount,
      loan_term_months: termMonths
    })
  })
  
  return await response.json()
}

async function handleUSSDMenu(request: USSDRequest): Promise<string> {
  // Get or create session
  const { data: session, error } = await supabase
    .rpc('get_or_create_session', {
      p_session_id: request.sessionId,
      p_phone_number: request.phoneNumber
    })
  
  if (error) throw error
  
  const menuState: MenuState = session.session_data || { step: 'start' }
  const input = request.text.trim()
  
  try {
    switch (menuState.step) {
      case 'start':
        return `CON Welcome to FarmIQ Loans
1. Check loan eligibility
2. Apply for loan
3. Check loan status
4. Make payment`
      
      case 'check_eligibility':
        const farmerData = await getFarmerProfile(request.phoneNumber)
        if (!farmerData) {
          return `END Please register at your local cooperative first.`
        }
        
        const creditScore = await checkCreditScore(farmerData)
        return `END Credit Score Report:
Score: ${(creditScore.credit_score * 100).toFixed(0)}%
Status: ${creditScore.approved ? 'Eligible' : 'Not eligible'}
Max loan: ${creditScore.max_loan_amount?.toFixed(0) || 0} KES`
      
      case 'loan_amount':
        const amount = parseFloat(input)
        if (isNaN(amount)) {
          return `CON Enter loan amount (KES):`
        }
        menuState.loanRequest = { amount }
        menuState.step = 'loan_term'
        await updateSession(request.sessionId, menuState)
        return `CON Enter loan term (months):`
      
      case 'loan_term':
        const months = parseInt(input)
        if (isNaN(months)) {
          return `CON Enter valid number of months:`
        }
        
        const farmer = await getFarmerProfile(request.phoneNumber)
        const simulation = await simulateLoan(
          farmer,
          menuState.loanRequest.amount,
          months
        )
        
        if (!simulation.approved) {
          return `END Loan simulation failed:
${simulation.reason}

Recommendations:
${simulation.recommendations.join('\n')}`
        }
        
        return `END Loan approved!
Amount: ${simulation.loan_details.amount} KES
Term: ${simulation.loan_details.term_months} months
Monthly payment: ${simulation.loan_details.monthly_payment.toFixed(0)} KES

Visit your cooperative to complete application.`
      
      default:
        menuState.step = 'start'
        await updateSession(request.sessionId, menuState)
        return handleUSSDMenu(request)
    }
  } catch (error) {
    console.error('USSD Error:', error)
    return 'END An error occurred. Please try again later.'
  }
}

async function updateSession(sessionId: string, menuState: MenuState) {
  const { error } = await supabase
    .from('ussd_sessions')
    .update({ session_data: menuState })
    .eq('session_id', sessionId)
  
  if (error) throw error
}

serve(async (req) => {
  try {
    const ussdRequest: USSDRequest = await req.json()
    const response = await handleUSSDMenu(ussdRequest)
    
    return new Response(response, {
      headers: { 'Content-Type': 'text/plain' },
    })
  } catch (error) {
    console.error('Error:', error)
    return new Response('END System Error', {
      headers: { 'Content-Type': 'text/plain' },
    })
  }
})