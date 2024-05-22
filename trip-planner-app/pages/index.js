import { useState, useEffect } from 'react';
import Results from './results.js';

export default function Home() {
    const [tripType, setTripType] = useState('');
    const [budget, setBudget] = useState('');
    const [fromDate, setFromDate] = useState('');
    const [toDate, setToDate] = useState('');
    const [isFormValid, setIsFormValid] = useState(false);
    const [resultData, setResultData] = useState(null);
    const [formData, setFormData] = useState(null);

    const today = new Date().toISOString().split('T')[0];

    useEffect(() => {
        handleFieldChange();
    }, [fromDate, toDate]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formCurrentData = {
            trip_type: tripType,
            budget: budget,
            from_date: fromDate,
            to_date: toDate
        };

        await setFormData(formCurrentData);

        try {
            const response = await fetch('http://localhost:8000/process_data/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formCurrentData)
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

    const handleNewSearch = () => {
        // Reset form fields and result data
        setTripType('');
        setBudget('');
        setFromDate('');
        setToDate('');
        setResultData(null);
    };

    return (
        <div className="container">

            {resultData ? (
                <Results resultData={resultData} formData={formData} handleNewSearch={handleNewSearch} />
            ) : (
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
            )}
        </div>
    );

}
