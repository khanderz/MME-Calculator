"use strict";

console.log('js is working');

const tr = $(document.createElement('tr'));

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

// should implment sevenDayAvg like updateTotalMME (line 8)
let sevenDayAvg = 0

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
        incrementSevenDay();
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
        let now = moment().format('YYYY-MM-DD')
        let sevenDaysAgo = new Date()
        sevenDaysAgo = moment(sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)).format('YYYY-MM-DD')
        let input = moment(medData.date_filled)
        let dateWithinWeek = moment(medData.date_filled).isBetween(sevenDaysAgo, now);
        
        if (dateWithinWeek) {
            sevenDayAvg += data.MME
            console.log(sevenDayAvg, '7 DAY AVERAGE')
        }
        
        updateTotalMME();
        incrementSevenDay();
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
            alert('Medication added to your database. You can now view the medication in your user details page.');
        } else {
            alert('Please login');
        }
    });
};

// Reset med list button
const clearMedList = () => {
    $('#med-list').empty();
    updateTotalMME();
    incrementSevenDay();
};


// Clinical assessment pop-up
const clinicalAssessment = (MMETotal) => {
    console.log(MMETotal, '&&&&&&CLINICAL ASSESSMENT&&&&&')
    if (MMETotal <= 20) {
        // alert('Acceptable therapeutic range');
        $('#assessment').html('Acceptable therapeutic range');
    } if (MMETotal >= 50) {
        // alert('Use extra precautions such as: monitor and assess pain and function more frequently; discuss reducing dose or tapering and discontinuing opioids if benefits do not outweigh harms; consider non-opioid alternatives; consider prescribing naloxone')     
        $('#assessment').html('Use extra precautions such as: monitor and assess pain and function more frequently; discuss reducing dose or tapering and discontinuing opioids if benefits do not outweigh harms; consider non-opioid alternatives; consider prescribing naloxone');
    } if (MMETotal >= 90) {
        // alert('Avoid, carefully justify dose, increase monitoring, and consider prescribing naloxone')
        $('#assessment').html('Avoid, carefully justify dose, increase monitoring, and/or consider prescribing naloxone')
}};

// EVENT LISTENERS
document.getElementById('drug-form').addEventListener('submit', handleCalculate);
document.getElementById('save-list-button').addEventListener('click', handleSaveList);
document.getElementById('clear-med-list').addEventListener('click', clearMedList);


// FEATURES
// 7 day daily average feature
// MME sum [(today + 7 days from med.date_filled) divided by 7]

// function sevenDay() {
//     let dateFilled = $('#date_filled').val()
//     let drugName = $('#drug').val()
//     let dose = $('#dose').val()
//     let quantity = $('#quantity').val()
//     let days_supply = $('#days_supply').val()

//     console.log(dateFilled)

//     let args = {
//         'date': dateFilled,
//         'drug': drugName,
//         'dose': dose,
//         'quantity': quantity,
//         'days_supply': days_supply
//     }

//     $.get('/get-seven-day-avg', args, (res) => {
//         // check if dateFilled < today and dateFilled > than 7 days ago then send request 
//         tr.append(`<td class="med-list-sevenday">${res.seven_avg}</td>`);
//         console.log(res);
//         console.log(res.seven_avg);
        
//         // Append tr to #med-list
//         $('#med-list').append(tr);

//         // $('#7day-mme-total').html(Number(res.seven_avg))
        
//     })
// };

const incrementSevenDay = () => {
    let sevenDay = 0;


    // Get all .med-list-mme <td> elements
    $('.med-list-sevenday').each((idx, el) => {
        console.log(el);

        sevenDay += Number($(el).html());
        
        console.log(`Total after 7-day loop # ${idx}: ${sevenDay}`);
    });

    $('#7day-mme-total').html(sevenDayAvg);
};