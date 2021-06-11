console.log('js is working')

const handleCalculate = (event) => {
    event.preventDefault()
    const params = {
        'drug': document.querySelector('#drug').value,
        'dose': document.querySelector('#dose').value,
        'quantity': document.querySelector('#quantity').value, 
        'days_supply': document.querySelector('#days_supply').value
    }

    console.log(params)

    $.get('/results', params, (data) => {
        console.log(data, '*********DATA*******')
        $('#mme-total').html(data.MME)
    })

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
const handleAddMed = (event) => {
    event.preventDefault()
    const formData = {
        'drug': document.querySelector('#drug').value,
        'dose': document.querySelector('#dose').value,
        'quantity': document.querySelector('#quantity').value, 
        'days_supply': document.querySelector('#days_supply').value    
    }
    console.log(formData)

    $.post('/add', formData, (response) => {
        console.log(response)
    })
}


document.getElementById('drug-form').addEventListener('submit', handleCalculate)
document.getElementById('add-med-button').addEventListener('click', handleAddMed)