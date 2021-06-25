"use strict";

// Create button element, add click handler to remove associated medlist row
// and recalculate + display MME total and clinical assessment.
const buildMedlistRowDeleteButton = () => {
    // Create delete button
    const button = $(document.createElement('button'));
    button.html('Delete drug');

    // Add event handler to delete button that deletes the button's row
    $(button).on('click', (evt) => {
        // Get the button's row and delete it
        const rowToDelete = $(button).parent();
        rowToDelete.remove();

        const MMETotal = calculateTotalMME();
        displayMMETotal(MMETotal);
        displayClinicalAssessment(MMETotal);
    });
    
    return button;
};

// Recalculate/update total MME based on meds in #med-list
const calculateTotalMME = () => {
    let MMETotal = 0;

    // Get all .med-list-mme <td> elements
    $('.med-list-mme').each((idx, el) => {
        console.log(el);

        MMETotal += Number($(el).html());
        
        console.log(`Total after loop # ${idx}: ${MMETotal}`);
    });

    return MMETotal;
};

// Display clinical assessment message based on total MME.
const displayClinicalAssessment = (MMETotal) => {
    console.log(MMETotal, '&&&&&&CLINICAL ASSESSMENT&&&&&');
    
    const LOW_MME_MSG = 'Acceptable therapeutic range';
    const MED_MME_MSG = 'Use extra precautions such as: monitor and assess pain and function more frequently; discuss reducing dose or tapering and discontinuing opioids if benefits do not outweigh harms; consider non-opioid alternatives; consider prescribing naloxone';
    const HIGH_MME_MSG = 'Avoid, carefully justify dose, increase monitoring, and/or consider prescribing naloxone';

    if (MMETotal <= 20) {
        $('#assessment').html(LOW_MME_MSG);
    } else if (MMETotal >= 50) {
        $('#assessment').html(MED_MME_MSG);
    } else if (MMETotal >= 90) {
        $('#assessment').html(HIGH_MME_MSG);
    }
};

const displayMMETotal = (MMETotal) => {
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
//     date_filled: date filled
//  }
const addMedToMedlist = (medData) => {

    
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
        tr.append(buildMedlistRowDeleteButton());
        
        // Append tr to #med-list
        $('#med-list').append(tr);
        
        const MMETotal = calculateTotalMME();

        displayMMETotal(MMETotal);
        displayClinicalAssessment(MMETotal);
    });
};

// takes user inputs and assigns them to "params"
const handleCalculate = (event) => {
    event.preventDefault();

    const params = {
        'drug': $('#drug').val(),
        'dose': $('#dose').val(),
        'quantity': $('#quantity').val(), 
        'days_supply': $('#days_supply').val(),
        'date_filled': $('#date_filled').val()
    };

    console.log(params);
    addMedToMedlist(params);
};

// takes in user inputs and assigns it "formData"
const handleSaveList = (event) => {
    event.preventDefault();

    const formData = {
        'drug': $('#drug').val(),
        'dose': $('#dose').val(),
        'quantity': $('#quantity').val(), 
        'days_supply': $('#days_supply').val(), 
        'date_filled': $('#date_filled').val()
    };

    console.log(formData);

    // sevenDay();

    // adds to user.med_list in db
    $.post('/add', formData, (response) => {
        console.log(response);
        if (response.msg === 'medication added') {
            addMedToMedlist(formData);
            alert('Medication added to your database. You can now view the medication in your user dashboard.');
        } else {
            alert('Please login');
        }
    });
};

// Reset med list button
const clearMedList = () => {
    $('#med-list').empty();

    const MMETotal = calculateTotalMME();

    displayMMETotal(MMETotal);
    displayClinicalAssessment(MMETotal);
};



// EVENT LISTENERS
document.getElementById('drug-form').addEventListener('submit', handleCalculate);
document.getElementById('save-list-button').addEventListener('click', handleSaveList);
document.getElementById('clear-med-list').addEventListener('click', clearMedList);