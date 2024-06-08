from datetime import datetime

from fastapi import APIRouter, Depends

from config import Config, error_message
from crud.listing import (
    fetch_all_listings,
    fetch_all_listings_of_user,
    fetch_listing_by_id,
    insert_listing,
    update_listing,
    delete_listing,
    delete_user_listings,
    delete_all_listings,
)
from crud.user import fetch_user_by_id
from schemas import ListingAdd, ListingUpdate, ListingView
from authentication.authentication_handler import get_current_user


listings = APIRouter(prefix=f'{Config.LISTINGS_PREFIX}')


@listings.get('/getListing/{listing_id}', tags=['Listing'], response_model=ListingView | dict[str, str])
async def get_listing(listing_id: str) -> dict[str, str]:
    """Get a listing by its id."""
    response = await fetch_listing_by_id(listing_id)
    if response:
        return response
    raise error_message[400]


@listings.get('/getUserListings/{user_id}', tags=['Listing'], response_model=list[ListingView] | list[dict[str, str]])
async def get_user_listings(user_id: str = Depends(get_current_user)) -> list[dict[str, str]]:
    """Get all the listings registered by the current logged-in user."""
    response = await fetch_all_listings_of_user(user_id)
    if response:
        return response
    raise error_message[400]


@listings.get('/getAllListings/', tags=['Listing'], response_model=list[ListingView] | list[dict[str, str]])
async def get_all_listings() -> list[dict[str, str]]:
    """Get all the registered listings."""
    response = await fetch_all_listings()
    if response:
        return response
    raise error_message[400]


@listings.post('/addListing/', tags=['Listing'])
async def add_listing(listing: ListingAdd, user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Add a new listing for the current logged-in user."""
    current_time = datetime.utcnow()

    listing = listing.dict()
    listing.update({
        'owner_id': user_id,
        'created_at': current_time,
        'updated_at': current_time,
    })

    response = await insert_listing(listing)
    if response:
        return response
    raise error_message[400]


@listings.put('/updateListing/', tags=['Listing'])
async def edit_listing(listing: ListingUpdate, listing_id: str, user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Edit a listing's availability by its id."""
    listing_in_database = await fetch_listing_by_id(listing_id)

    if not user_id == listing_in_database.get('user_id'):
        raise error_message[401]
    
    listing.update({'updated_at': datetime.utcnow()})
    response = await update_listing(listing_id, **listing)
    if response:
        return response
    raise error_message[400]


@listings.delete('/deleteListing/', tags=['Listing'])
async def remove_listing(listing_id: str, user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Delete a listing by its id."""
    listing_in_database = await fetch_listing_by_id(listing_id)

    if user_id != listing_in_database.get('owner_id'):
        raise error_message[401]

    response = await delete_listing(listing_id)
    if response:
        return response
    raise error_message[400]


@listings.delete('/deleteUserListings/', tags=['Listing'])
async def remove_user_listings(user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Delete all the listings registered by the current logged-in user."""
    response = await delete_user_listings(user_id)
    if response:
        return response
    raise error_message[400]


@listings.delete('/deleteAllListings/', tags=['Listing'])
async def remove_all_listings(user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """[SUPERUSER-ONLY] Delete all the registered listings."""
    current_user = fetch_user_by_id(user_id)
    if current_user.get('is_supermodel') == False:
        raise error_message[403]

    response = await delete_all_listings()
    if response:
        return response
    raise error_message[400]
