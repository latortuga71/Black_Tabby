{
  "_id": "_design/final",
  "views": {
    "agent": {
      "map": "function (doc) {\n  emit(doc._id, {\"agent_id\":doc.agent_id, \"OS\":doc.os, \"IP\":doc.ip});\n}"
    }
  },
  "language": "javascript"
}
