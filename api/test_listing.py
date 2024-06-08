from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_all_listings():
    response = client.get('api/v1/listings/getAllListings/')
    assert response.status_code == 200


# def test_get_listing():
#     example_id = '12ae17134a394c2a8d621604689a42ce'
#     response = client.get(f'api/v1/listings/getListing/{example_id}/')
#     assert response.status_code == 200
#     assert response.json() == {
#         "type": "HOUSE",
#         "available_now": True,
#         "address": "string",
#         "id": "12ae17134a394c2a8d621604689a42ce",
#         "created_at": "2023-07-08T07:16:07.289911+00:00",
#         "updated_at": "2023-07-08T07:16:07.289911+00:00",
#     }


# def test_get_wrong_listing():
#     example_id = '-1'
#     response = client.get(f'api/v1/listings/getListing/{example_id}/')
#     assert response.status_code == 200
#     assert response.json() == {
#         "NoListingsFoundError": "No listing was found with this id",
#     }
