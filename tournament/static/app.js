Vue.use(Vuetable);

let tableData = JSON.parse(document.getElementById('tableData').textContent);
let groupList = Object.keys(tableData);

let app = new Vue({
  el: '#app',
  delimiters: ["[[", "]]"],
  data: {
    message: 'Hello Vue!',
    selectedGroup: groupList[0],
    group_list: groupList
  },
  methods: {
    dataManager: function () {
      return tableData[this.selectedGroup]
    }
  }
});

app.$watch('selectedGroup', function (newValue, oldValue) {
  this.$refs.vuetable.refresh();
});
