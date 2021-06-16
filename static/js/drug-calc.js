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
};

// Add medication to medlist table
// Args:
// medData (object) - an object that looks like:
//   {
//     drug: drug name,
//     dose: drug dose,
//     quantity: quantity of drug,
//     days_supply: days supply
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
        'days_supply': document.querySelector('#days_supply').value
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
        'days_supply': document.querySelector('#days_supply').value    
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

// event listeners
document.getElementById('drug-form').addEventListener('submit', handleCalculate);
document.getElementById('save-list-button').addEventListener('click', handleSaveList);
document.getElementById('clear-med-list').addEventListener('click', clearMedList);