import {
  getTomorow,
  getDayInWeek,
  convertDate,
  convertTime,
  getCurrentDate,
  fomatDateTime,
} from '@/lib/common.js';

export function getListDates() {
  const list = [];
  let i = 0;
  let d = new Date();
  while (i < 2) {
    const dayInWeek = getDayInWeek(d);
    if (dayInWeek === 'Thứ 7') {
      i += 1;
    }
    const day = {
      date: convertDate(d, 'YYYY-MM-DD'),
      dayOfWeek: dayInWeek,
      statusDate: 'not-choose',
    };
    list.push(day);
    d = getTomorow(d);
  }
  return list;
}
export function getListTimeInDay() {
  const list = [
    {
      id: 1, start: '09:00', stop: '09:30', statusTime: 'empty',
    },
    {
      id: 2, start: '09:30', stop: '10:00', statusTime: 'empty',
    },
    {
      id: 3, start: '10:00', stop: '10:30', statusTime: 'empty',
    },
    {
      id: 4, start: '10:30', stop: '11:00', statusTime: 'empty',
    },
    {
      id: 5, start: '11:00', stop: '11:30', statusTime: 'empty',
    },
    {
      id: 6, start: '11:30', stop: '12:00', statusTime: 'empty',
    },
    {
      id: 7, start: '13:00', stop: '13:30', statusTime: 'empty',
    },
    {
      id: 8, start: '13:30', stop: '14:00', statusTime: 'empty',
    },
    {
      id: 9, start: '14:00', stop: '14:30', statusTime: 'empty',
    },
    {
      id: 10, start: '14:30', stop: '15:00', statusTime: 'empty',
    },
    {
      id: 11, start: '15:00', stop: '15:30', statusTime: 'empty',
    },
    {
      id: 12, start: '15:30', stop: '16:00', statusTime: 'empty',
    },
    {
      id: 13, start: '16:00', stop: '16:30', statusTime: 'empty',
    },
    {
      id: 14, start: '16:30', stop: '17:00', statusTime: 'empty',
    },
    {
      id: 15, start: '17:00', stop: '17:30', statusTime: 'empty',
    },
    {
      id: 16, start: '17:30', stop: '18:00', statusTime: 'empty',
    },
  ];
  return list;
}
export function setBackgroundBeyondTimes(list, date) {
  for (let i = 0; i < list.length; i += 1) {
    const dateTimeNow = convertDate(getCurrentDate(), 'YYYY-MM-DDTHH:mm:ss');
    const dateTime = fomatDateTime(date, list[i].start);
    if (dateTime < dateTimeNow) {
      list[i].statusTime = 'enabled';
    }
  }
}

export function setBackgroundVisibleTimesByDate(list, startTime, stopTime, statusTime) {
  const s = convertDate(startTime, 'HH:mm');
  const f = convertDate(stopTime, 'HH:mm');
  for (let i = 0; i < list.length; i += 1) {
    if (list[i].start >= s && list[i].stop <= f) {
      list[i].statusTime = statusTime;
    }
  }
}

export function setBackgroundVisibleTimesByTime(list, startTime, stopTime, statusTime) {
  const s = convertTime(startTime, 'HH:mm');
  const f = convertTime(stopTime, 'HH:mm');
  for (let i = 0; i < list.length; i += 1) {
    if (list[i].start >= s && list[i].stop <= f) {
      list[i].statusTime = statusTime;
    }
  }
}

export function listNumbers() {
  const list = [
    { name: 1 },
    { name: 2 },
    { name: 3 },
    { name: 4 },
    { name: 5 },
    { name: 6 },
    { name: 7 },
    { name: 8 },
    { name: 9 },
    { name: 10 },
    { name: 11 },
    { name: 12 },
  ];
  return list;
}

export function listPeriods() {
  const list = [
    { name: 'Ngày', id: 1 },
    { name: 'Tuần', id: 2 },
    { name: 'Tháng', id: 3 },
    { name: 'Năm', id: 4 },
  ];
  return list;
}
