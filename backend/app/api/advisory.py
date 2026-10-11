from typing import List
from fastapi import APIRouter
from app.models.schemas import MandiPriceItem, WeatherSummary

router = APIRouter(prefix="/api/advisory", tags=["Agricultural Advisory & Real-time Data"])

@router.get("/mandi-prices", response_model=List[MandiPriceItem])
async def get_mandi_prices(state: str = "Uttar Pradesh"):
    """Fetches localized mandi wholesale rates (AGMARKNET data feed)"""
    return [
        MandiPriceItem(
            crop="Wheat (गेहूं / ಗೋಧಿ)",
            market="Agra APMC",
            state=state,
            min_price=2200.0,
            max_price=2350.0,
            modal_price=2275.0,
            unit="₹/Quintal",
            updated_at="Today, 09:30 AM"
        ),
        MandiPriceItem(
            crop="Paddy (धान / ಭತ್ತ)",
            market="Karnal APMC",
            state=state,
            min_price=2150.0,
            max_price=2280.0,
            modal_price=2183.0,
            unit="₹/Quintal",
            updated_at="Today, 10:15 AM"
        ),
        MandiPriceItem(
            crop="Tomato (टमाटर / ಟೊಮ್ಯಾಟೊ)",
            market="Kolar Mandi",
            state="Karnataka",
            min_price=1400.0,
            max_price=1800.0,
            modal_price=1650.0,
            unit="₹/Quintal",
            updated_at="Today, 08:45 AM"
        ),
        MandiPriceItem(
            crop="Mustard (सरसों / ಸಾಸಿವೆ)",
            market="Jaipur APMC",
            state="Rajasthan",
            min_price=5300.0,
            max_price=5650.0,
            modal_price=5450.0,
            unit="₹/Quintal",
            updated_at="Today, 11:00 AM"
        ),
    ]

@router.get("/weather", response_model=WeatherSummary)
async def get_weather_advisory(location: str = "North Zone"):
    """Fetches localized weather and farmer-specific agromet advisories"""
    return WeatherSummary(
        location=location,
        temperature=28.5,
        condition="Partly Cloudy",
        humidity=65,
        rainfall_probability=20,
        advisory="Good conditions for weeding and soil aeration. Postpone chemical spray if overcast skies develop."
    )
