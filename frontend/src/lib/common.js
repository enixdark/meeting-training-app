import moment from 'moment';

export function chunkInefficient(arr, len) {
  const chunks = [];
  let i = 0;
  const n = arr.length;
  while (i < n) {
    chunks.push(arr.slice(i, i += len));
  }
  return chunks;
}

export function getDayInWeek(time) {
  const d = moment(time).day();
  if (d === 0) {
    const weekDay = 'Chủ Nhật';
    return weekDay;
  }
  const weekDay = `Thứ ${d + 1}`;
  return weekDay;
}
export function getCurrentDate() {
  return moment().toDate();
}
export function getTomorow(date) {
  return moment(date).add(1, 'days');
}
export function convertDate(date, format) {
  if (date === null) return '';
  return moment(date).format(format);
}
export function convertTime(time, format) {
  if (time === null) return '';
  return moment(time, 'HH:mm:ss').format(format);
}
export function getTime(startTime, stopTime) {
  return moment(stopTime).diff(moment(startTime), 'minutes');
}
export function fomatDateTime(date, time) {
  const d = moment(date).format('YYYY-MM-DD');
  return moment(`${d} ${time}`).format('YYYY-MM-DDTHH:mm:ss');
}
export function fomatDate(date) {
  return moment(date, 'DD-MM-YYYY').format('YYYY-MM-DD');
}
