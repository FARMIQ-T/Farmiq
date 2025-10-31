from typing import Dict, List, Optional, Any
from supabase import create_client, Client
import os
from datetime import datetime
import uuid

class DatabaseService:
    def __init__(self, url: str, key: str):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(url, key)

    # Farmer Operations
    async def create_farmer(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new farmer profile"""
        response = await self.supabase.table('farmers').insert(farmer_data).execute()
        return response.data[0] if response.data else None

    async def get_farmer(self, farmer_id: str) -> Dict[str, Any]:
        """Get farmer profile by ID"""
        response = await self.supabase.table('farmers').select('*').eq('id', farmer_id).execute()
        return response.data[0] if response.data else None

    async def update_farmer(self, farmer_id: str, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update farmer profile"""
        response = await self.supabase.table('farmers').update(farmer_data).eq('id', farmer_id).execute()
        return response.data[0] if response.data else None

    # Farm Operations
    async def create_farm(self, farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new farm record"""
        response = await self.supabase.table('farms').insert(farm_data).execute()
        return response.data[0] if response.data else None

    async def get_farm(self, farm_id: str) -> Dict[str, Any]:
        """Get farm details by ID"""
        response = await self.supabase.table('farms').select('*').eq('id', farm_id).execute()
        return response.data[0] if response.data else None

    async def get_farms_by_farmer(self, farmer_id: str) -> List[Dict[str, Any]]:
        """Get all farms owned by a farmer"""
        response = await self.supabase.table('farms').select('*').eq('farmer_id', farmer_id).execute()
        return response.data

    # Crop Operations
    async def create_crop(self, crop_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new crop record"""
        response = await self.supabase.table('crops').insert(crop_data).execute()
        return response.data[0] if response.data else None

    async def get_crops_by_farm(self, farm_id: str) -> List[Dict[str, Any]]:
        """Get all crops for a farm"""
        response = await self.supabase.table('crops').select('*').eq('farm_id', farm_id).execute()
        return response.data

    # Financial Records Operations
    async def create_financial_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new financial record"""
        response = await self.supabase.table('financial_records').insert(record_data).execute()
        return response.data[0] if response.data else None

    async def get_financial_records(self, farmer_id: str, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """Get financial records for a farmer within a date range"""
        query = self.supabase.table('financial_records').select('*').eq('farmer_id', farmer_id)
        if start_date:
            query = query.gte('record_date', start_date)
        if end_date:
            query = query.lte('record_date', end_date)
        response = await query.execute()
        return response.data

    # Credit Score Operations
    async def create_credit_score(self, score_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new credit score record"""
        response = await self.supabase.table('credit_scores').insert(score_data).execute()
        return response.data[0] if response.data else None

    async def get_latest_credit_score(self, farmer_id: str) -> Dict[str, Any]:
        """Get the latest credit score for a farmer"""
        response = await self.supabase.table('credit_scores').select('*').eq('farmer_id', farmer_id).order('score_date', desc=True).limit(1).execute()
        return response.data[0] if response.data else None

    # Resource Operations
    async def create_resource(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new resource record"""
        response = await self.supabase.table('resources').insert(resource_data).execute()
        return response.data[0] if response.data else None

    async def get_resources_by_farm(self, farm_id: str) -> List[Dict[str, Any]]:
        """Get all resources for a farm"""
        response = await self.supabase.table('resources').select('*').eq('farm_id', farm_id).execute()
        return response.data

    # Loan Operations
    async def create_loan(self, loan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new loan record"""
        response = await self.supabase.table('loans').insert(loan_data).execute()
        return response.data[0] if response.data else None

    async def get_loans_by_farmer(self, farmer_id: str) -> List[Dict[str, Any]]:
        """Get all loans for a farmer"""
        response = await self.supabase.table('loans').select('*').eq('farmer_id', farmer_id).execute()
        return response.data

    async def update_loan_status(self, loan_id: str, status: str) -> Dict[str, Any]:
        """Update loan status"""
        response = await self.supabase.table('loans').update({'status': status}).eq('id', loan_id).execute()
        return response.data[0] if response.data else None