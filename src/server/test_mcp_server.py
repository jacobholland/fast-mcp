#!/usr/bin/env python3
"""Quick test script for your MCP server"""

import asyncio
import sys
sys.path.append('.')

from DataManager import DataManager

async def test_basic_functionality():
    """Test the basic data flow"""
    print("🧪 Testing DataManager...")
    
    # Test with in-memory DB for quick testing
    dm = DataManager(":memory:")
    
    # Test data insertion
    test_data = {
        'location': 'Test City',
        'temperature': 25.5,
        'humidity': 60.0,
        'pressure': 1013.25,
        'description': 'Clear skies',
        'raw_api_response': {'test': True}
    }
    
    try:
        rows = dm.insert_weather_data(test_data)
        print(f"✅ Inserted {rows} rows")
        
        # Test query
        results = dm.execute_query("SELECT * FROM raw_weather")
        print(f"✅ Queried {len(results)} rows")
        print(f"   First row: {results[0] if results else 'None'}")
        
        # Test table info
        count_result = dm.execute_query("SELECT COUNT(*) as count FROM raw_weather")
        print(f"✅ Total records: {count_result[0]['count']}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    print("🎉 Basic tests passed!")
    return True

async def test_weather_api():
    """Test the actual weather API call"""
    print("\n🌤️  Testing weather API...")
    
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://wttr.in/London?format=j1", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                current = data.get('current_condition', [{}])[0]
                print(f"✅ API working! London temp: {current.get('temp_C')}°C")
                return True
            else:
                print(f"❌ API returned: {response.status_code}")
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 Testing MCP Server Components\n")
    
    async def run_tests():
        basic_ok = await test_basic_functionality()
        api_ok = await test_weather_api()
        
        if basic_ok and api_ok:
            print("\n✅ All tests passed! Your MCP server should work.")
        else:
            print("\n❌ Some tests failed. Check the errors above.")
    
    asyncio.run(run_tests())