// https://stackoverflow.com/questions/41164672/whats-the-equivalent-of-angular-service-in-vuejs/54165192#54165192
// https://www.qcode.in/api-error-handling-in-vue-with-axios/

import axios from 'axios';
import localStorageService from '@/services/localStorageService'

let baseUrl = "http://localhost:8000/stattracker/api/v1";
let axiosInstance = null;

export default new class {
    
    constructor(){
        axiosInstance = axios.create({
            baseURL: baseUrl,            
            headers: { 'Content-Type': 'application/json' }  
        });
    }

    //#region User
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
    //#endregion

    //#region User Weight Stats
    getWeightStatsByUser(userId){

        let creds = localStorageService.getCredentialsModel();
        console.log("creds");
        console.log(creds);
        const config = {
            headers: { Authorization: `Bearer ${creds.access_token}` }
        };

        return axiosInstance(`/weightstats/${userId}`, config);
    }
    ////#endregion
 }