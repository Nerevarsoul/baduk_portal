Vue.use(Vuetable);

let tableData = JSON.parse(document.getElementById('tableData').textContent);
let groupList = Object.keys(tableData);

let fields = Object.keys(tableData[groupList[0]][0]);

let app = new Vue({
  el: '#app',
  delimiters: ["[[", "]]"],
  data: {
    message: 'Hello Vue!',
    fields: fields,
    selectedGroup: groupList[0],
    group_list: groupList,
    sortOrder: [
      {
        field: 'wins',
        direction: 'asc'
      }
    ]
  },
  methods: {
    dataManager: function () {
      this.fields = Object.keys(tableData[this.selectedGroup][0]);
      console.log(this.fields);
      return tableData[this.selectedGroup]
    }
  }
});

app.$watch('selectedGroup', function (newValue, oldValue) {
  this.$refs.vuetable.refresh();
});
