// https://stackoverflow.com/questions/41164672/whats-the-equivalent-of-angular-service-in-vuejs/54165192#54165192
// https://www.qcode.in/api-error-handling-in-vue-with-axios/

import axios from 'axios';

let baseUrl = "http://localhost:8000/stattracker/api/v1";
let axiosInstance = null;

export default new class {
    
    constructor(){
        axiosInstance = axios.create({
            baseURL: baseUrl,            
            headers: { 'Content-Type': 'application/json' }  
        });
    }

    //#region Students
    getUsers(){
        return axiosInstance("/users");
    }

    getUserById(userId){
        return axiosInstance(`/users/${userId}`);
    }

    createUser(user){
        return axiosInstance.post("/users", user);
    }

    authenticate(creds){
        return axiosInstance.post("/authenticate", creds);
    }

    // saveStudent(item){
    //     return axiosInstance.post("/users", item);
    // }
    //#endregion
 }