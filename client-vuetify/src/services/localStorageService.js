// https://stackoverflow.com/questions/41164672/whats-the-equivalent-of-angular-service-in-vuejs/54165192#54165192
// https://www.qcode.in/api-error-handling-in-vue-with-axios/

export default new class {

    //#region Token
    tokenTitle = "token";
    setToken(token){
        window.localStorage.setItem(this.tokenTitle, token);
        //window.localStorage.setItem(this.tokenTitle, JSON.stringify(token));
    }
    getToken(){
        return window.localStorage.getItem(this.tokenTitle);
        //return JSON.parse(window.localStorage.getItem(this.tokenTitle));
    }
    removeToken(){
        return window.localStorage.removeItem(this.tokenTitle);
    }
    ////#endregion

    //#region User
    userTitle = "user";
    setUser(user){
        window.localStorage.setItem(this.userTitle, JSON.stringify(user));
    }
    getUser(){
        return JSON.parse(window.localStorage.getItem(this.userTitle));
    }
    removeUser(){
        return window.localStorage.removeItem(this.userTitle);
  }
    ////#endregion    

 }