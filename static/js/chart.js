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


// WEEKLY CHART
const convertToWeeklyChartData = (medList) => {
  const today = moment();
  const sevenDaysAgo = moment().subtract(7, 'days');
  console.log(`today: ${today}`);
  console.log(`sevenDaysAgo: ${sevenDaysAgo}`);
  const days = generateDatesForRange(
    sevenDaysAgo.format('YYYY-MM-DD'),
    today.format('YYYY-MM-DD')
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

    // for each date of datesActive
      // use date to index into dateAndTotalMME
      // increment value stored there by med.daily_MME
    for (const date of datesActive) {
      dateAndTotalMME[date] += med.daily_MME;
    }  
  } 
  
  const chartData = [];
  for (const [ date, totalMME ] of Object.entries(dateAndTotalMME)) {
    chartData.push({x: date, y: totalMME});
  }
  
  return chartData;
};


$.get('/api/med_list', (medList) => {
  const data = convertToWeeklyChartData(medList);

  new Chart(
    $('#week-bar-chart'),
    {
      type: 'bar',
      data: {
        datasets: [
          {
            label: '7 Day Total Daily MME',
            data: data
          }
        ]
      },
      options: {
        datasets: {
          bar: {
            backgroundColor: () => {
              return randomColor();
            }
          }
        },
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
});





// MONTHLY CHART
const convertToMonthlyChartData = (medList) => {
  const firstDayOfMonth = moment().date(1);
  console.log(`firstDayOfMonth: ${firstDayOfMonth}`);
  const days = generateDatesForRange(
    firstDayOfMonth.format('YYYY-MM-DD'),
    firstDayOfMonth.add(30, 'days').format('YYYY-MM-DD')
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

    // for each date of datesActive
      // use date to index into dateAndTotalMME
      // increment value stored there by med.daily_MME
    for (const date of datesActive) {
      dateAndTotalMME[date] += med.daily_MME;
    }
  }  
  
  const chartData = [];
  for (const [ date, totalMME ] of Object.entries(dateAndTotalMME)) {
    chartData.push({x: date, y: totalMME});
  }
  
  return chartData;
};

$.get('/api/med_list', (medList) => {
  const data = convertToMonthlyChartData(medList);

  new Chart(
    $('#month-bar-chart'),
    {
      type: 'bar',
      data: {
        datasets: [
          {
            label: '30 Day Total Daily MME',
            data: data
          }
        ]
      },
      options: {
        datasets: {
          bar: {
            backgroundColor: () => {
              return randomColor();
            }
          }
        },
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
});

