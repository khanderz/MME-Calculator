"use strict";

console.log('js is working');

// Recalculate/update total MME based on meds in #med-list
const updateTotalMME = () => {
    let MMETotal = 0;

    // Get all .med-list-mme <td> elements
    $('.med-list-mme').each((idx, el) => {
        console.log(el);

        MMETotal += Number($(el).html());
        
        console.log(`Total after loop # ${idx}: ${MMETotal}`);
    });

    $('#mme-total').html(MMETotal);

    clinicalAssessment(MMETotal);

// REACT hook to update clinical assessment
    // assessment(MMETotal);
};

// Add medication to medlist table
// Args:
// medData (object) - an object that looks like:
//   {
//     drug: drug name,
//     dose: drug dose,
//     quantity: quantity of drug,
//     days_supply: days supply 
//     date_filled: date filled
//  }
const addMedToMedlist = (medData) => {
    // Create delete button
    const button = $(document.createElement('button'));
    button.html('Delete drug');

    // Add event handler to delete button that deletes the button's row
    $(button).on('click', (evt) => {
        // Get the button's row and delete it
        const rowToDelete = $(button).parent();
        rowToDelete.remove();

        updateTotalMME();
    });
    
    // Build tr element
    const tr = $(document.createElement('tr'));
    tr.attr('class', 'medication');

    // Append data from medData to row
    tr.append(`
        <td class="med-list-drug">${medData.drug}</td>
        <td>${medData.dose}</td>
        <td>${medData.quantity}</td>
        <td>${medData.days_supply}</td>
        <td>${medData.date_filled}</td>
    `);
    
    // Calculate MME for medData and add to #med-list table
    $.get('/results', medData, (data) => {
        tr.append(`<td class="med-list-mme">${data.MME}</td>`);
        tr.append(button);
        
        // Append tr to #med-list
        $('#med-list').append(tr);
        updateTotalMME();

    });
};

// takes user inputs and assigns them to "params"
const handleCalculate = (event) => {
    event.preventDefault();

    const params = {
        'drug': $('#drug').val(),
        'dose': document.querySelector('#dose').value,
        'quantity': document.querySelector('#quantity').value, 
        'days_supply': document.querySelector('#days_supply').value,
        'date_filled': document.querySelector('#date_filled').value
    };

    console.log(params);
    
    addMedToMedlist(params);
    
};

// takes in user inputs and assigns it "formData"
const handleSaveList = (event) => {
    event.preventDefault();

    const formData = {
        'drug': document.querySelector('#drug').value,
        'dose': document.querySelector('#dose').value,
        'quantity': document.querySelector('#quantity').value, 
        'days_supply': document.querySelector('#days_supply').value, 
        'date_filled': document.querySelector('#date_filled').value   
    };

    console.log(formData);

    // adds to user.med_list in db
    $.post('/add', formData, (response) => {
        console.log(response);
        if (response.msg === 'medication added') {
            addMedToMedlist(formData);
        }
    });
};

// Reset med list button
const clearMedList = () => {
    $('#med-list').empty();
    updateTotalMME();
};


// Clinical assessment pop-up
const clinicalAssessment = (MMETotal) => {
    console.log(MMETotal, '&&&&&&CLINICAL ASSESSMENT&&&&&')
    if (MMETotal <= 20) {
        alert('Acceptable therapeutic range');
    } if (MMETotal >= 50) {
        alert('Use extra precautions such as: monitor and assess pain and function more frequently; discuss reducing dose or tapering and discontinuing opioids if benefits do not outweigh harms; consider non-opioid alternatives; consider prescribing naloxone')     
    } if (MMETotal >= 90) {
        alert('Avoid, carefully justify dose, increase monitoring, and consider prescribing naloxone')
}};

// EVENT LISTENERS
document.getElementById('drug-form').addEventListener('submit', handleCalculate);
document.getElementById('save-list-button').addEventListener('click', handleSaveList);
document.getElementById('clear-med-list').addEventListener('click', clearMedList);


// FEATURES
// 7 day daily average feature
// MME sum [(today + 7 days from med.date_filled) divided by 7]
const sevenDay = () => {
    today = Date();
    const [month, day, year] = [date.getMonth(), date.getDate(), date.getFullYear()];
    
}




// REACT
// function results() {

//     const [assessValue, setAssessValue] = React.useState('There is no completely safe opioid dose; use caution when prescribing opioids at any dose and always prescribe the lowest effective dose.');

//     function assessment(MMETotal) {
//         if (MMETotal <= 20) {
//             setAssessValue('Acceptable therapeutic range');
//         } if (MMETotal >= 50) {
//             setAssessValue('Use extra precautions such as: monitor and assess pain and function more frequently; discuss reducing dose or tapering and discontinuing opioids if benefits do not outweigh harms; consider non-opioid alternatives; consider prescribing naloxone')     
//         } if (MMETotal >= 90) {
//             setAssessValue('Avoid, carefully justify dose, increase monitoring, and consider prescribing naloxone')
//     }};

//     return ({assessValue})
// }    

// REACT state change to render clinical assessment per Total MME 
// ReactDOM.render(
//     assessment(), document.getElementById('assessment')
// );