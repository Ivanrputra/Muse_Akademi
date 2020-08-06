Vue.config.devtools = false;
Vue.config.productionTip = false;

const nav = new Vue({
  el: "#nav",
  data: {
    showBtnBottom: false,
    showSearchInput: false,
    showSidebar: false,
  },
  methods: {
    submitItem(id){
          document.getElementById(id).submit();
     }
}
});
