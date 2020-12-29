// https://stackoverflow.com/questions/41164672/whats-the-equivalent-of-angular-service-in-vuejs/54165192#54165192
// https://www.qcode.in/api-error-handling-in-vue-with-axios/

export default new class {

    //#region Credentials
    tokenTitle = "tokenCredentials";
    setCredentialsModel(token){
        window.localStorage.setItem(this.tokenTitle, JSON.stringify(token), 1);
    }
    getCredentialsModel(){
        return JSON.parse(window.localStorage.getItem(this.tokenTitle));
    }
    removeCredentialsModel(){
        return window.localStorage.removeItem(this.tokenTitle);
  }
    ////#endregion
 }