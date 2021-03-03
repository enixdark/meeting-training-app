import moment from 'moment';
import { convertDate, fomatDateTime } from '@/lib/common.js';
import { getListDates } from '@/lib/listTimes.js';
import userServices from '@/lib/userServices.js';

export function getListMeetingInToday(listMeeting) {
  const emailUser = userServices.userData().user.email;
  const list = [];
  for (let i = 0; i < listMeeting.length; i += 1) {
    let isAccepted = null;
    let meetingSelected = null;
    let notConfirmSelected = null;
    let notAcceptedSelected = null;
    let acceptedSelected = null;
    let notAdhereSelected = null;
    let isConfirmActionSelected = null;
    let mayRequest = null;
    let meetingDuplicates = null;
    if (listMeeting[i].meeting === undefined) {
      isAccepted = listMeeting[i].attendees.filter(p => p.user.email === emailUser);
      meetingSelected = listMeeting[i];
      mayRequest = null;
      meetingDuplicates = [];
    } else {
      isAccepted = listMeeting[i].meeting.attendees.filter(p => p.user.email === emailUser);
      meetingSelected = listMeeting[i].meeting;
      mayRequest = listMeeting[i].may_request;
      meetingDuplicates = listMeeting[i].duplicates;
    }
    if (isAccepted.length !== 0) {
      if (!isAccepted[0].is_accepted) {
        if (isAccepted[0].is_response) {
          notConfirmSelected = false;
          notAcceptedSelected = true;
          acceptedSelected = false;
          isConfirmActionSelected = 'not-accepted';
        } else {
          notConfirmSelected = true;
          notAcceptedSelected = false;
          acceptedSelected = false;
          isConfirmActionSelected = 'accepted-false';
        }
      } else {
        notConfirmSelected = false;
        notAcceptedSelected = false;
        acceptedSelected = true;
        isConfirmActionSelected = 'accepted-true';
      }
      notAdhereSelected = false;
    } else {
      notAdhereSelected = true;
      notAcceptedSelected = false;
      acceptedSelected = false;
      notConfirmSelected = false;
      isConfirmActionSelected = 'accepted-none';
    }
    if (meetingSelected.state === false) {
      notAdhereSelected = false;
      notAcceptedSelected = false;
      acceptedSelected = false;
      notConfirmSelected = false;
      isConfirmActionSelected = 'accepted-false';
    }
    const content = {
      meeting: meetingSelected,
      isShowActionMenu: false,
      isConfirmAction: isConfirmActionSelected,
      notConfirm: notConfirmSelected,
      notAccepted: notAcceptedSelected,
      accepted: acceptedSelected,
      notAdhere: notAdhereSelected,
      may_request: mayRequest,
      duplicates: meetingDuplicates,
    };
    list.push(content);
  }
  return list;
}

export function groupMeetingByDates(list) {
  const listDates = getListDates();
  const meetingFutureAll = [];
  for (let i = 0; i < listDates.length; i += 1) {
    const listMeetingInDay = list.filter(p => convertDate(p.meeting.started_time, 'YYYY-MM-DD') === listDates[i].date);
    const oneDay = {
      date: listDates[i].date,
      meetings: null,
    };
    oneDay.meetings = listMeetingInDay;
    if (oneDay.meetings.length > 0) {
      meetingFutureAll.push(oneDay);
    }
  }
  return meetingFutureAll;
}

export function resetAllMeetings(listMeetingOnGoing, listMeetingToDay, listMeetingFuture) {
  for (let i = 0; i < listMeetingOnGoing.length; i += 1) {
    listMeetingOnGoing[i].isShowActionMenu = false;
  }
  for (let i = 0; i < listMeetingToDay.length; i += 1) {
    listMeetingToDay[i].isShowActionMenu = false;
  }
  for (let i = 0; i < listMeetingFuture.length; i += 1) {
    for (let j = 0; j < listMeetingFuture[i].meetings.length; j += 1) {
      listMeetingFuture[i].meetings[j].isShowActionMenu = false;
    }
  }
}

export function getMyMeetings(list) {
  const emailUser = userServices.userData().user.email;
  const listMyMeetings = [];
  list.forEach((meeting) => {
    const attendeesMeeting = meeting.attendees;
    const ismyMeeting = attendeesMeeting.filter(p => p.user.email === emailUser);
    if (ismyMeeting.length !== 0) {
      listMyMeetings.push(meeting);
    }
  });
  return listMyMeetings;
}

export function formatDataMeeting(numberPeriodic, dataMeeting) {
  let startTime = '';
  let stopTime = '';
  if (dataMeeting.typeMeeting === true) {
    if (dataMeeting.periodicId === 1 || dataMeeting.periodicId === 2) {
      startTime = fomatDateTime(moment(dataMeeting.startDate).add(numberPeriodic, 'days'), dataMeeting.startTime);
      stopTime = fomatDateTime(moment(dataMeeting.startDate).add(numberPeriodic, 'days'), dataMeeting.stopTime);
    } else if (dataMeeting.periodicId === 3) {
      startTime = fomatDateTime(moment(dataMeeting.startDate).add(numberPeriodic, 'months'), dataMeeting.startTime);
      stopTime = fomatDateTime(moment(dataMeeting.startDate).add(numberPeriodic, 'months'), dataMeeting.stopTime);
    } else {
      startTime = fomatDateTime(moment(dataMeeting.startDate).add(numberPeriodic, 'years'), dataMeeting.startTime);
      stopTime = fomatDateTime(moment(dataMeeting.startDate).add(numberPeriodic, 'years'), dataMeeting.stopTime);
    }
  } else {
    startTime = fomatDateTime(dataMeeting.startDate, dataMeeting.startTime);
    stopTime = fomatDateTime(dataMeeting.startDate, dataMeeting.stopTime);
  }
  const meeting = {
    name: dataMeeting.title,
    description: dataMeeting.description,
    location_id: dataMeeting.locationId,
    started_time: startTime,
    finished_time: stopTime,
    attendees: dataMeeting.listMailAttendees,
  };
  return meeting;
}

export function getListMeetingPeriodics(dataMeeting) {
  const list = [];
  const numberDays = moment(dataMeeting.stopDate).diff(moment(dataMeeting.startDate), 'day') + 1;
  const numberMonths = moment(dataMeeting.stopDate).diff(moment(dataMeeting.startDate), 'month') + 1;
  const numberYears = moment(dataMeeting.stopDate).diff(moment(dataMeeting.startDate), 'year') + 1;
  // Định kì theo ngày
  if (dataMeeting.periodicId === 1) {
    for (let i = 0; i < numberDays; i += dataMeeting.numberPeriodic) {
      const meeting = formatDataMeeting(i, dataMeeting);
      list.push(meeting);
    }
  }
  // Định kì theo tuần
  if (dataMeeting.periodicId === 2) {
    for (let i = 0; i < numberDays; i += 7 * dataMeeting.numberPeriodic) {
      const meeting = formatDataMeeting(i, dataMeeting);
      list.push(meeting);
    }
  }
  // Định kì theo tháng
  if (dataMeeting.periodicId === 3) {
    for (let i = 0; i < numberMonths; i += dataMeeting.numberPeriodic) {
      const meeting = formatDataMeeting(i, dataMeeting);
      list.push(meeting);
    }
  }
  // Định kì theo năm
  if (dataMeeting.periodicId === 4) {
    for (let i = 0; i < numberYears; i += dataMeeting.numberPeriodic) {
      const meeting = formatDataMeeting(i, dataMeeting);
      list.push(meeting);
    }
  }

  return list;
}

export function shearchMeetings(isComponent, dataShearch, listMeetings) {
  let listMeetingShearchs = null;
  if (dataShearch.text === '') {
    if (isComponent !== 3) {
      listMeetingShearchs = listMeetings.filter(
        p => convertDate(p.started_time, 'YYYY-MM-DD') === dataShearch.date,
      );
    } else {
      listMeetingShearchs = listMeetings.filter(
        p => convertDate(p.meeting.started_time, 'YYYY-MM-DD') === dataShearch.date,
      );
    }
  }
  if (dataShearch.date === '') {
    if (isComponent !== 3) {
      listMeetingShearchs = listMeetings.filter(
        p => p.name.includes(dataShearch.text),
      );
    } else {
      listMeetingShearchs = listMeetings.filter(
        p => p.meeting.name.includes(dataShearch.text),
      );
    }
  } else if (isComponent !== 3) {
    listMeetingShearchs = listMeetings.filter(
      p => p.name.includes(dataShearch.text) && convertDate(p.started_time, 'YYYY-MM-DD') === dataShearch.date,
    );
  } else {
    listMeetingShearchs = listMeetings.filter(
      p => p.meeting.name.includes(dataShearch.text) && convertDate(p.meeting.started_time, 'YYYY-MM-DD') === dataShearch.date,
    );
  }
  return listMeetingShearchs;
}

export function getDataSearch(isShearch, amountSelected, textShearch, dateShearch) {
  if (isShearch) {
    return {
      amount: amountSelected,
      data: {
        text: textShearch,
        date: convertDate(dateShearch, 'YYYY-MM-DD'),
      },
    };
  }
  return {
    amount: amountSelected,
    data: null,
  };
}
