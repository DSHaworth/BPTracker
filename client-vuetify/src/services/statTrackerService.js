// https://stackoverflow.com/questions/41164672/whats-the-equivalent-of-angular-service-in-vuejs/54165192#54165192
// https://www.qcode.in/api-error-handling-in-vue-with-axios/

import axios from 'axios';
import store from '@/store'

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

    getAuthorizationHeader(){
        return {
            headers: { 
                'Content-Type': 'application/json',
                Authorization: `Bearer ${store.state.token}` 
            }
        };
    }

    //#region User Weight Stats
    getWeightStatsByUser(userId){
        return axiosInstance(`/weightstats/${userId}`, this.getAuthorizationHeader());
    }

    addWeightStatForUser(weightStat){
        return axiosInstance.post(`/weightstats`, weightStat, this.getAuthorizationHeader());
    }    

    deleteWeightStatForUser(weightStat){
        return axiosInstance.delete(`/weightstats/${weightStat.userId}/${weightStat.weightId}`, this.getAuthorizationHeader());
    } 

    updateWeightStatForUser(weightStat){
        return axiosInstance.post(`/weightstats/${weightStat.userId}/${weightStat.weightId}`, weightStat, this.getAuthorizationHeader());
    }        
    ////#endregion
 }