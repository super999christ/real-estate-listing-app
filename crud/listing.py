from uuid import uuid4

from sqlalchemy import insert, update, delete
from sqlalchemy.future import select

from models import Listing
from database import db, transaction
from utils.bulk_query_handler import bulk_query_to_dict


async def fetch_all_listings() -> list[dict[str, str]]:
    """Fetch all listings from the database."""
    query = select(Listing)
    listings = await db.execute(query)
    listings = listings.scalars().all()
    if not listings:
        return [{'NoListingsFoundError': 'No listings are recorded'}]
    return bulk_query_to_dict(listings)


async def fetch_all_listings_of_user(owner_id: str) -> list[dict[str, str]]:
    """Fetch all the listings of a specific user from the database."""
    query = select(Listing).where(Listing.owner_id == owner_id)
    listings = await db.execute(query)
    listings = listings.scalars().all()
    if not listings:
        return [{'NoListingsFoundError': 'No listing was added by the current user'}]
    return bulk_query_to_dict(listings)


async def fetch_listing_by_id(id: str) -> dict[str, str]:
    """Fetch a certain listing by its id from the database."""
    query = select(Listing).where(Listing.id == id)
    listing = await db.execute(query)
    listing = listing.scalar()
    if listing:
        listing = listing.__dict__
        return listing
    return {'NoListingsFoundError': 'No listing was found with this id'}


async def insert_listing(listing: dict) -> dict[str, str]:
    """Insert a new listing inside the database."""
    listing.update({'id': uuid4().hex})  # first add a new random ID to the listing values
    stmt = insert(Listing).values(**listing)
    
    await db.execute(stmt)
    return await transaction(msg=f'Listing successfully added: {listing}')


async def update_listing(id: str, **kwargs) -> dict[str, str]:
    """Update a certain listing by its id with new information (only the availability)."""
    stmt = (
        update(Listing)
        .where(Listing.id == id)
        .values(**kwargs)
        .execution_options(synchronize_session='fetch')
    )

    await db.execute(stmt)
    return await transaction(msg='Listing successfully updated')


async def delete_listing(id: str) -> dict[str, dict[str, str] | str]:
    """Delete a certain listing by its id from the database."""
    stmt = delete(Listing).where(Listing.id == id).returning(Listing.id, Listing.owner_id)
    affected_row = await db.execute(stmt)
    affected_row = affected_row.first()

    if affected_row is not None:
        return await transaction(f'Listing successully deleted: {affected_row}')
    return {'NoListingsFoundError': 'No listing was found with this id'}


async def delete_user_listings(owner_id: str) -> dict[str, dict[str, str] | str]:
    """Delete all of the listings of a certain user by its id from the database."""
    stmt = delete(Listing).where(Listing.owner_id == owner_id).returning(Listing.id, Listing.owner_id)
    affected_row = await db.execute(stmt)
    affected_row = affected_row.first()

    if affected_row is not None:
        return await transaction(f'All listings successully deleted')
    return {'NoListingsFoundError': 'No listings exist for the user to be deleted'}


async def delete_all_listings() -> dict[str, str]:
    """Delete all of the listings inside the database."""
    stmt = delete(Listing).returning(Listing.id, Listing.owner_id)
    affected_row = await db.execute(stmt)
    affected_row = affected_row.first()

    if affected_row:
        return await transaction(f'All listings successully deleted')
    return {'NoListingsFoundError': 'No listings exist to be deleted'}
