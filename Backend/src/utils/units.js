// ======================================
// UNIT CONVERSION UTILITIES
// ======================================


// ======================================
// CELSIUS → FAHRENHEIT
// ======================================

const celsiusToFahrenheit = (celsius) => {
  if (typeof celsius !== "number") {
    return null;
  }

  return (celsius * 9) / 5 + 32;
};


// ======================================
// FAHRENHEIT → CELSIUS
// ======================================

const fahrenheitToCelsius = (fahrenheit) => {
  if (typeof fahrenheit !== "number") {
    return null;
  }

  return ((fahrenheit - 32) * 5) / 9;
};


// ======================================
// METERS → KILOMETERS
// ======================================

const metersToKilometers = (meters) => {
  if (typeof meters !== "number") {
    return null;
  }

  return meters / 1000;
};


// ======================================
// KILOMETERS → METERS
// ======================================

const kilometersToMeters = (kilometers) => {
  if (typeof kilometers !== "number") {
    return null;
  }

  return kilometers * 1000;
};


// ======================================
// METERS → NAUTICAL MILES
// ======================================

const metersToNauticalMiles = (meters) => {
  if (typeof meters !== "number") {
    return null;
  }

  return meters / 1852;
};


// ======================================
// KILOMETERS → NAUTICAL MILES
// ======================================

const kilometersToNauticalMiles = (kilometers) => {
  if (typeof kilometers !== "number") {
    return null;
  }

  return kilometers / 1.852;
};


// ======================================
// NAUTICAL MILES → KILOMETERS
// ======================================

const nauticalMilesToKilometers = (
  nauticalMiles
) => {
  if (typeof nauticalMiles !== "number") {
    return null;
  }

  return nauticalMiles * 1.852;
};


// ======================================
// METERS/SECOND → KNOTS
// ======================================

const metersPerSecondToKnots = (metersPerSecond) => {
  if (typeof metersPerSecond !== "number") {
    return null;
  }

  return metersPerSecond * 1.943844;
};


// ======================================
// KNOTS → METERS/SECOND
// ======================================

const knotsToMetersPerSecond = (knots) => {
  if (typeof knots !== "number") {
    return null;
  }

  return knots * 0.514444;
};


// ======================================
// MILLIMETERS → METERS
// ======================================

const millimetersToMeters = (millimeters) => {
  if (typeof millimeters !== "number") {
    return null;
  }

  return millimeters / 1000;
};


// ======================================
// ROUND VALUE
// ======================================

const roundValue = (value, decimals = 2) => {
  if (typeof value !== "number") {
    return null;
  }

  const multiplier =
    Math.pow(10, decimals);

  return (
    Math.round(value * multiplier) /
    multiplier
  );
};


// ======================================
// EXPORT
// ======================================

module.exports = {

  celsiusToFahrenheit,

  fahrenheitToCelsius,

  metersToKilometers,

  kilometersToMeters,

  metersToNauticalMiles,

  kilometersToNauticalMiles,

  nauticalMilesToKilometers,

  metersPerSecondToKnots,

  knotsToMetersPerSecond,

  millimetersToMeters,

  roundValue,

};