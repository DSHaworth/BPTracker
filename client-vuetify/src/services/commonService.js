export default new class{

    formatDate(dateToFormat){
        return new Date(dateToFormat).toLocaleDateString(); 
    }

    formatDateTime(dateToFormat){
        let thisDate = new Date(dateToFormat);
        return thisDate.toLocaleString();  
    }

    getLastRecordedDateDays(recordDateTime){
        let lastDate = new Date(recordDateTime); 
        let today = new Date(); 
        
        // To calculate the time difference of two dates 
        var Difference_In_Time = today.getTime() - lastDate.getTime(); 

        // To calculate the no. of days between two dates 
        let diff = Difference_In_Time / (1000 * 3600 * 24);

        if(diff < 1){
            return "Last recorded less than a day";
        } 
        else if (diff < 2)
        {
            return "Last recorded a day ago";
        } 
        return `${parseInt(diff)} days ago`;
    }

    groupBy(list, keyGetter) {
        const map = new Map();
        list.forEach((item) => {
             const key = keyGetter(item);
             const collection = map.get(key);
             if (!collection) {
                 map.set(key, [item]);
             } else {
                 collection.push(item);
             }
        });
        return map;
    }
}