const DataSnapshot = require("../models/DataSnapshot");

const saveSnapshot = async ({
  analysisId,
  zoneId,
  source,
  variable,
  value = null,
  unit = null,
  validAt = null,
  dataType = null,
  quality = null,
  status = "available",
}) => {
  const snapshot = await DataSnapshot.create({
    analysisId,
    zoneId,
    source,
    variable,
    value,
    unit,
    validAt,
    retrievedAt: new Date(),
    dataType,
    quality,
    status,
  });

  return snapshot;
};

const saveSnapshots = async (snapshots = []) => {
  if (!Array.isArray(snapshots) || snapshots.length === 0) {
    return [];
  }

  return DataSnapshot.insertMany(snapshots);
};

const getSnapshots = async (analysisId, zoneId = null) => {
  const query = {
    analysisId,
  };

  if (zoneId) {
    query.zoneId = zoneId;
  }

  return DataSnapshot.find(query)
    .sort({ retrievedAt: -1 })
    .lean();
};

module.exports = {
  saveSnapshot,
  saveSnapshots,
  getSnapshots,
};