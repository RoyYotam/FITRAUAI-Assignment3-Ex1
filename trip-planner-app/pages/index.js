import { useState, useEffect } from 'react';

export default function Home() {
    const [tripType, setTripType] = useState('');
    const [budget, setBudget] = useState('');
    const [fromDate, setFromDate] = useState('');
    const [toDate, setToDate] = useState('');
    const [isFormValid, setIsFormValid] = useState(false);
    const [resultData, setResultData] = useState(null);

    const today = new Date().toISOString().split('T')[0];

    useEffect(() => {
        handleFieldChange();
    }, [fromDate, toDate]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = {
            trip_type: tripType,
            budget: budget,
            from_date: fromDate,
            to_date: toDate
        };

        try {
            const response = await fetch('http://localhost:8000/process_data/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setResultData(data);

        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Validate form fields
    const validateForm = () => {
        return tripType !== '' && budget !== '' && fromDate !== '' && toDate !== '' && toDate > fromDate;
    };

    // Update form validity on field changes
    const handleFieldChange = () => {
        setIsFormValid(validateForm());
    };

    return (
        <div className="container">
            <div className="formContainer">
                <h1 className="title">Plan Your Dream Vacation</h1>
                <form onSubmit={handleSubmit}>
                    <div className="formItem">
                        <label className="label">
                            Choose Your Trip Type:
                            <select value={tripType} onChange={(e) => {setTripType(e.target.value); handleFieldChange();}} id="tripType">
                                <option value="">Select Trip Type</option>
                                <option value="Beach">Beach</option>
                                <option value="Ski">Ski</option>
                                <option value="City">City</option>
                            </select>
                        </label>
                    </div>
                    <div className="formItem">
                        <label className="label">
                            Estimated Budget (USD):
                            <input type="number" value={budget} onChange={(e) => {setBudget(e.target.value); handleFieldChange();}} className="inputField" />
                        </label>
                    </div>
                    <div className="formItem">
                        <label className="label">
                            Departure Date:
                            <input type="date" min={today} value={fromDate} onChange={(e) => {setFromDate(e.target.value);}} className="inputField" />
                        </label>
                    </div>
                    <div className="formItem">
                        <label className="label">
                            Return Date:
                            <input type="date" min={fromDate} value={toDate} onChange={(e) => {setToDate(e.target.value);}} className="inputField" />
                        </label>
                    </div>
                    <button type="submit" className="button" disabled={!isFormValid}>Let's Go!</button>
                </form>
            </div>

            {resultData && (
                <div className="resultContainer">
                    {resultData.map((result, index) => (
                        <div key={index}>
                            <h2>Option {index + 1}</h2>
                            {/* Display flights */}
                            <h3>Flights:</h3>
                            {result.from_flight && (
                                <div className="flight">
                                    {/* Display from_flight details */}
                                    <p>From Flight:</p>
                                    <p>Airline: {result.from_flight.airline}</p>
                                    <p>Flight Number: {result.from_flight.flight_number}</p>
                                    {/* Add more flight details as needed */}
                                </div>
                            )}
                            {result.to_flight && (
                                <div className="flight">
                                    {/* Display to_flight details */}
                                    <p>To Flight:</p>
                                    <p>Airline: {result.to_flight.airline}</p>
                                    <p>Flight Number: {result.to_flight.flight_number}</p>
                                    {/* Add more flight details as needed */}
                                </div>
                            )}
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
                </div>
            )}

        </div>
    );

}
