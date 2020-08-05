new Vue({
  el: "#base",
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
Vue.config.devtools = false;
Vue.config.productionTip = false;