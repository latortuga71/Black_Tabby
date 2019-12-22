{
  "_id": "_design/final",
  "views": {
    "agent": {
      "map": "function (doc) {\n  emit(doc._id, {\"agent_id\":doc._agent_id, \"OS\":doc.OS, \"IP\":doc.ip});\n}"
    }
  },
  "language": "javascript"
}