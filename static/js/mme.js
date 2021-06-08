// add drug to med list and calculation of MME

"use strict";

// add drug to medication list
document.querySelector('form').addEventListener('submit', (evt) => {
  evt.preventDefault();
  
 $('#med-list').append(`
  <tr>
      <td> 
      ${document.querySelector('#drug-field').value} 
      ${document.querySelector('#dose-field').value} 
      ${document.querySelector('#quantity-field').value} 
      ${document.querySelector('#days-supply-field').value} 
      </td>
  </tr>
  `);
});

// reset medication list and total MME
const resetList = () => {
    $('#mme-total').html('0.00');
    $('#med-list').empty();
  };



// const incrementMMETotal = (MME) => {
//   const mmeTotal = $('#mme-total');

//   let total = Number(mmeTotal.html());
//   total += mme;

//   mmeTotal.html(total.toFixed(2));
// };

const populateMME = (results) => {
  $('#mme-total').html(results.MME);
  };

