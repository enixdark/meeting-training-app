// eslint-disable-next-line import/prefer-default-export
export function listDataByRoom(listData) {
  const datas = [];
  for (let i = 0; i < listData.length; i += 1) {
    const listMeetings = [];
    listData[i].ListMeetingByRoom.forEach((p) => {
      const meeting = {
        start: p.started_time,
        end: p.finished_time,
        meeting: p,
      };
      listMeetings.push(meeting);
    });
    // eslint-disable-next-line no-shadow
    const template = {
      name: listData[i].locationName,
      address: listData[i].loactionAddress,
      colorPair: i % 2 === 0 ? '#3a8ee6' : '#FF647C',
      gtArray: listMeetings,
    };
    datas.push(template);
  }
  return datas;
}
