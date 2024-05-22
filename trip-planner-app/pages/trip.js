// pages/trip.js

import React, { useState, useEffect } from 'react';


const Trip = ({ chosenResult, dailyTripResult, handleNewSearch }) => {

    return (
        <div>
            <button onClick={handleNewSearch} className="closeButton">X</button>
            <h1>Trip Plan</h1>
            <div>
                <h2>Total Cost: {chosenResult.total_price}</h2>

                {/* Display flights */}
                <h2>Flights:</h2>
                <h3>To</h3>
                {chosenResult.to_flight.flights.map((flight, flightIndex) => (
                    <div key={flightIndex} className="flight">
                        <p>Flight {flightIndex + 1}</p>
                        <p>Airline: {flight.airline}, {flight.flight_number}</p>
                        <p>{flightIndex !== chosenResult.to_flight.flights.length - 1 ? "-----" : ""}</p>
                        {/* Add more flight details as needed */}
                    </div>
                ))}
                {/* Display layovers */}
                <h3>Layovers:</h3>
                {chosenResult.to_flight.layovers.map((layover, layoverIndex) => (
                    <div key={layoverIndex} className="layover">
                        <p>Airport: {layover.name}</p>
                        <p>Duration: {layover.duration} minutes</p>
                        <p>{layoverIndex !== chosenResult.to_flight.layovers.length - 1 ? "-----" : ""}</p>
                    </div>
                ))}
                {/* Display other details */}
                <h3>Other Details:</h3>
                <p>Total Duration: {chosenResult.to_flight.total_duration} minutes</p>

                <p>----------------------------------------</p>


                <h3>From</h3>
                {chosenResult.from_flight.flights.map((flight, flightIndex) => (
                    <div key={flightIndex} className="flight">
                        <p>Flight {flightIndex + 1}</p>
                        <p>Airline: {flight.airline}, {flight.flight_number}</p>
                        <p>{flightIndex !== chosenResult.from_flight.flights.length - 1 ? "-----" : ""}</p>
                        {/* Add more flight details as needed */}
                    </div>
                ))}
                {/* Display layovers */}
                <h3>Layovers:</h3>
                {chosenResult.from_flight.layovers.map((layover, layoverIndex) => (
                    <div key={layoverIndex} className="layover">
                        <p>Airport: {layover.name}</p>
                        <p>Duration: {layover.duration} minutes</p>
                        <p>{layoverIndex !== chosenResult.from_flight.layovers.length - 1 ? "-----" : ""}</p>
                    </div>
                ))}
                {/* Display other details */}
                <h3>Other Details:</h3>
                <p>Total Duration: {chosenResult.from_flight.total_duration} minutes</p>

                {/* Display hotel */}
                <h3>Hotel:</h3>
                {chosenResult.hotel && (
                    <div className="hotel">
                        {/* Display hotel details */}
                        <p>Name: {chosenResult.hotel.name}</p>
                        <p>Description: {chosenResult.hotel.description}</p>
                        {/* Add more hotel details as needed */}
                    </div>
                )}

                {/* Display daily plan */}
                <h2>Daily Plan:</h2>
                {dailyTripResult && dailyTripResult.DayTripInfo &&(
                    <div>
                        {dailyTripResult.DayTripInfo.map((day_of_trip, index) => (
                            <div>
                                <h3>Date: {day_of_trip.Date}</h3>
                                <h3>Activities:</h3>
                                <ul>
                                    {day_of_trip.Activities.map((activity, index) => (
                                        <li key={index}>
                                            {activity.TimeOnDay} - {activity.Activity}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>
                )}

                {/* Display images */}
                <h2>Images:</h2>
                {dailyTripResult && dailyTripResult.images_paths &&
                    dailyTripResult.images_paths.map((path, index) => (
                    <img key={index} src={`http://localhost:8000${path}`} alt={`Image ${index + 1}`}
                         className="dayTripImage"/>
            ))}
        </div>
        </div>
    );
};

export default Trip;
