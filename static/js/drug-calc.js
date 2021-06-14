console.log('js is working')



// takes user inputs and assigns them to "params"

// create a reset button that will reset MMECalcTotal back to 0
let MMECalcTotal = 0

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
        MME = data.MME
        incrementMME(MME);
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
}

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

// event listeners
document.getElementById('drug-form').addEventListener('submit', handleCalculate)
document.getElementById('add-med-button').addEventListener('click', handleAddMed)