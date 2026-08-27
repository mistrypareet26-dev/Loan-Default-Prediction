const form = document.getElementById("prediction-form");
const resultBox = document.getElementById("prediction-result");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const loanData = {
        loan_amnt: Number(document.getElementById("loan_amnt").value),
        int_rate: Number(document.getElementById("int_rate").value),
        installment: Number(document.getElementById("installment").value),
        grade: document.getElementById("grade").value,
        home_ownership: document.getElementById("home_ownership").value,
        annual_inc: Number(document.getElementById("annual_inc").value),
        verification_status:
            document.getElementById("verification_status").value,
        purpose: document.getElementById("purpose").value,
        dti: Number(document.getElementById("dti").value),
        term_class: document.getElementById("term_class").value,
        emp_class: document.getElementById("emp_class").value
    };

    console.log("Sending to API:", loanData);

    resultBox.innerHTML = `
        <p> Predicting...</p>
    `;

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(loanData)
            }
        );

        const result = await response.json();

        console.log("API response:", result);

        if (!response.ok) {
            throw new Error(result.detail || "Prediction failed");
        }

        if (result.error) {
            throw new Error(result.error);
        }


        resultBox.innerHTML = `
    <div class="prediction-output">

        <div class="prediction-head">
            <h3>Prediction Result</h3>
        </div>

        <div class="prediction-para">

            <p>
                <strong>Prediction:</strong>
                ${result.prediction}
            </p>

            <p>
                <strong>Default Probability:</strong>
                ${(result.default_probability * 100).toFixed(2)}%
            </p>

        </div>

    </div>
`;
    } catch (error) {
        console.error("Prediction error:", error);

        resultBox.innerHTML = `
            <h3>Prediction Error</h3>
            <p> ${error.message}</p>
        `;
    }
});