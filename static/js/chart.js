"use strict";

// [
//   {
//     "daily_MME": 0.75, 
//     "date_filled": "2021-06-17",
//     "days_supply": 5, 
//     "drug_dose": 5, 
//     "end_date": "2021-06-22", 
//     "med_id": 1, 
//     "opioid": {
//       "conversion_factor": 0.15, 
//       "opioid_name": "Codeine"
//     }, 
//     "quantity": 5, 
//     "user_id": 1
//   }
// ]
// moment.duration(30, "days").asDays();

// Generate array of dates for range.
//   generateDatesForRange('2021-06-01', '2021-06-30')
//   => ['2021-06-01', ..., '2021-06-30']
const generateDatesForRange = (start, end) => {
  const startDate = moment(start);
  const endDate = moment(end);

  const duration = Math.abs(moment
    .duration(startDate.diff(endDate))
    .asDays()
  );

  const dates = [startDate.format('YYYY-MM-DD')];

  while (dates.length != duration) {
    const latestDay = dates[dates.length - 1];
    const nextDay = moment(latestDay).add(1, 'days');
    
    dates.push(nextDay.format('YYYY-MM-DD'));
  }
  
  dates.push(endDate.format('YYYY-MM-DD'));
  
  return dates;
};

const convertToMonthlyChartData = (medList) => {
  const firstDayOfMonth = moment().date(1);
  const days = generateDatesForRange(
    firstDayOfMonth,
    firstDayOfMonth.add(30, 'days')
  );
  
  // Create dateAndTotalMME:
  //   date:       totalMME
  // { 2021-06-01: 0, 2021-06-02: 0}
  const dateAndTotalMME = {};
  for (const day of days) {
    dateAndTotalMME[day] = 0;
  }
  
  // for each med in medlist
    // generate range of dates starting at date_filled, end at end_date
  for (const med of medList) {
    console.log(`med: ${med.opioid.opioid_name}`);

    const datesActive = generateDatesForRange(med.date_filled, med.end_date);
    
    console.log(`datesActive: ${datesActive}`);
  } 
    // for each date in range of dates
      // use date to index into dateLookup
      // increment value stored there by med.daily_MME

  // Month starts on date 1, goes until end of month (day 30)
  // [
  //   {date: 2021-06-01, totalMME: 0}
    //   ...
  //   {date: 2021-06-17, totalMME: 0.75}
  //   {date: 2021-06-18, totalMME: 0}
};

$.get('/api/med_list', (medList) => {
  convertToMonthlyChartData(medList);
});

// Plot 30 day MME total
/*
$.get('/api/med_list', (medList) => {
  // x: a day in this month
  // y: total MME for that day
  const chartData = convertToMonthlyChartData(medList);

  // Also, to enable scaling by time, you need to import Moment *before*
  // Chart.js. See `templates/chartjs.html`.
  new Chart(
    $('#bar-chart'),
    {
      type: 'bar',
      data: {
        datasets: [
          {
            label: 'All Melons',
            data: data
          }
        ]
      },
      options: {
        scales: {
          xAxes: [
            {
              type: 'time',
              distribution: 'series'
            }
          ]
        }
      }
    }
  );
})*/