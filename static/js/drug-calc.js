console.log('js is working')

// create a reset button that will reset MMECalcTotal back to 0
let MMECalcTotal = 0

// takes user inputs and assigns them to "params"
const handleCalculate = (event) => {
    event.preventDefault()
    const params = {
        'drug': document.querySelector('#drug').value,
        'dose': document.querySelector('#dose').value,
        'quantity': document.querySelector('#quantity').value, 
        'days_supply': document.querySelector('#days_supply').value
    }

    console.log(params)

    // increment MME 
    const incrementMME = (MME) => {
        const MMEtotal = $('#mme-total')

        MMECalcTotal += MME
        
        console.log(MMECalcTotal)

        MMEtotal.html(MMECalcTotal);
        console.log(MME, '******* Increment MME *******')
    }

    // populates total MME
    $.get('/results', params, (data) => {
        console.log(data, '*********DATA*******');
        $('#mme-total').html(data.MME);
        MME = data.MME;
        incrementMME(MME);
        $('#med-list').append(`<tr> <td> ${data.MME} </td> </tr>`);
    })

    // appends med list
    $('#med-list').append(`
    <tr>
      <td> 
      ${document.querySelector('#drug').value} 
      ${document.querySelector('#dose').value} 
      ${document.querySelector('#quantity').value} 
      ${document.querySelector('#days_supply').value}
      </td>
    </tr>`);

    // create delete button
    const button = document.createElement("BUTTON");
        button.innerText = 'Delete drug';
    
    $('#med-list').append(`
    <tr>
      <td> 
      ${button}
      </td>
    </tr>`);
};

// takes in user inputs and assigns it "formData"
const handleAddMed = (event) => {
    event.preventDefault()
    const formData = {
        'drug': document.querySelector('#drug').value,
        'dose': document.querySelector('#dose').value,
        'quantity': document.querySelector('#quantity').value, 
        'days_supply': document.querySelector('#days_supply').value    
    }
    console.log(formData)

    // adds to user.med_list in db
    $.post('/add', formData, (response) => {
        console.log(response)
    })
}

// Reset med list button
const clearMedList = () => {
    $('#mme-total').html('0');
    $('#med-list').empty();
    MMECalcTotal = 0;
    console.log(MMECalcTotal, '******* MME total reset *******');
};

// Delete a drug from the med list
const deleteDrug =

// event listeners
document.getElementById('drug-form').addEventListener('submit', handleCalculate)
document.getElementById('add-med-button').addEventListener('click', handleAddMed)
document.getElementById('clear-med-list').addEventListener('click', clearMedList)


// REACT
// ReactDOM.render();