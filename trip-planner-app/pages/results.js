// pages/results.js

import React, { useState } from 'react';
import Trip from './trip'

const Results = ({ resultData, formData, handleNewSearch }) => {
    const [currentOption, setCurrentOption] = useState(0);
    const [dailyPlanResult, setDailyPlanResult] = useState(null);

    const handleNextOption = () => {
        setCurrentOption(prevOption => (prevOption + 1) % resultData.length);
    };

    const handlePreviousOption = () => {
        setCurrentOption(prevOption => (prevOption - 1 + resultData.length) % resultData.length);
    };

    const handleChoose = async (e) => {
        try {
            const dataToSend = {
                location: resultData[currentOption].city,
                from_date: formData.from_date,
                to_date: formData.to_date
            };

            const response = await fetch('http://localhost:8000/daily_plan/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            });

            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setDailyPlanResult(data);

        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="resultContainer">
            {dailyPlanResult ? (
                <Trip chosenResult={resultData[currentOption]} dailyTripResult={dailyPlanResult} handleNewSearch={handleNewSearch}/>
                ) : (
            <div>
                <button onClick={handleNewSearch} className="closeButton">X</button>
                {resultData && resultData.map((result, index) => (
                    <div key={index} className="resultItem"
                         style={{display: index === currentOption ? 'block' : 'none'}}>
                        <h1>{result.city}</h1>

                        {/* Display flights */}
                        <h2>Flights:</h2>
                        <h3>To</h3>
                        {result.to_flight && result.to_flight.flights &&
                            result.to_flight.flights.map((flight, flightIndex) => (
                            <div key={flightIndex} className="flight">
                                <p>Flight {flightIndex + 1}</p>
                                <p>Airline: {flight.airline}, {flight.flight_number}</p>
                                <p>{flightIndex !== result.to_flight.flights.length - 1 ? "-----" : ""}</p>
                                {/* Add more flight details as needed */}
                            </div>
                        ))}
                        {/* Display layovers */}
                        <h3>Layovers:</h3>
                        {result.to_flight && result.to_flight.flights &&
                            result.to_flight.layovers.map((layover, layoverIndex) => (
                            <div key={layoverIndex} className="layover">
                                <p>Airport: {layover.name}</p>
                                <p>Duration: {layover.duration} minutes</p>
                                <p>{layoverIndex !== result.to_flight.layovers.length - 1 ? "-----" : ""}</p>
                            </div>
                        ))}
                        {/* Display other details */}
                        <h3>Other Details:</h3>
                        <p>Total Duration: {result.to_flight.total_duration} minutes</p>

                        <p>----------------------------------------</p>


                        <h3>From</h3>
                        {result.from_flight && result.from_flight.flights &&
                            result.from_flight.flights.map((flight, flightIndex) => (
                            <div key={flightIndex} className="flight">
                                <p>Flight {flightIndex + 1}</p>
                                <p>Airline: {flight.airline}, {flight.flight_number}</p>
                                <p>{flightIndex !== result.from_flight.flights.length - 1 ? "-----" : ""}</p>
                                {/* Add more flight details as needed */}
                            </div>
                        ))}
                        {/* Display layovers */}
                        <h3>Layovers:</h3>
                        {result.from_flight && result.from_flight.flights &&
                            result.from_flight.layovers.map((layover, layoverIndex) => (
                            <div key={layoverIndex} className="layover">
                                <p>Airport: {layover.name}</p>
                                <p>Duration: {layover.duration} minutes</p>
                                <p>{layoverIndex !== result.from_flight.layovers.length - 1 ? "-----" : ""}</p>
                            </div>
                        ))}
                        {/* Display other details */}
                        <h3>Other Details:</h3>
                        <p>Total Duration: {result.from_flight.total_duration} minutes</p>

                        {/* Display hotel */}
                        <h3>Hotel:</h3>
                        {result.hotel && (
                            <div className="hotel">
                                {/* Display hotel details */}
                                <p>Name: {result.hotel.name}</p>
                                <p>Description: {result.hotel.description}</p>
                                {/* Add more hotel details as needed */}
                            </div>
                        )}
                    </div>
                ))}
                <div className="buttonContainer">
                    {currentOption > 0 &&
                        <button onClick={handlePreviousOption} className="transparentButton">Previous Page</button>}
                    <button onClick={handleChoose} className="chooseButton">Choose</button>
                    {currentOption < resultData.length - 1 &&
                        <button onClick={handleNextOption} className="transparentButton">Next Page</button>}
                </div>
            </div>
                )}
        </div>
    );
};

export default Results;