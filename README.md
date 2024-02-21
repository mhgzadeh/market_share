# Market Share Calculator

This FastAPI application calculates the market share of given points within a specified city boundary.

1. Reproject coordinates to utm
2. Check the intersection of point location to city boundary
3. Create 500m buffer 
4. Dissolved buffer area
5. Return the calculated the market share

## Installation

1. Clone the repository

2. Install the dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Make a POST request to the `/market-share/` endpoint with the city boundary and points data in the request body.

    Example:

    ```json
    {
      "city_boundary": {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [100.0, 0.0],
              [101.0, 0.0],
              [101.0, 1.0],
              [100.0, 1.0],
              [100.0, 0.0]
            ]
          ]
        }
      },
      "points": [
        [100.1, 0.1],
        [100.2, 0.2],
        [100.3, 0.3]
      ]
    }
    ```

3. The server will respond with the calculated market share:

    ```json
    {
      "market_share": 34.6
    }
    ```