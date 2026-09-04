// ======================================
// TIME UTILITIES
// ======================================


// ======================================
// GET CURRENT UTC TIME
// ======================================

const nowUTC = () => {
  return new Date();
};


// ======================================
// GET ISO TIMESTAMP
// ======================================

const nowISO = () => {
  return new Date().toISOString();
};


// ======================================
// CONVERT DATE TO ISO
// ======================================

const toISOString = (date) => {
  if (!date) {
    return null;
  }

  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return null;
  }

  return parsedDate.toISOString();
};


// ======================================
// CHECK VALID DATE
// ======================================

const isValidDate = (date) => {
  if (!date) {
    return false;
  }

  const parsedDate = new Date(date);

  return !Number.isNaN(parsedDate.getTime());
};


// ======================================
// GET DATE ONLY
// YYYY-MM-DD
// ======================================

const getDateOnly = (date = new Date()) => {
  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return null;
  }

  return parsedDate.toISOString().slice(0, 10);
};


// ======================================
// GET TIME ONLY
// HH:MM:SS
// ======================================

const getTimeOnly = (date = new Date()) => {
  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return null;
  }

  return parsedDate
    .toISOString()
    .slice(11, 19);
};


// ======================================
// ADD MINUTES
// ======================================

const addMinutes = (date, minutes) => {
  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return null;
  }

  if (typeof minutes !== "number") {
    return null;
  }

  return new Date(
    parsedDate.getTime() +
    minutes * 60 * 1000
  );
};


// ======================================
// ADD HOURS
// ======================================

const addHours = (date, hours) => {
  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return null;
  }

  if (typeof hours !== "number") {
    return null;
  }

  return new Date(
    parsedDate.getTime() +
    hours * 60 * 60 * 1000
  );
};


// ======================================
// EXPORT
// ======================================

module.exports = {
  nowUTC,
  nowISO,
  toISOString,
  isValidDate,
  getDateOnly,
  getTimeOnly,
  addMinutes,
  addHours,
};