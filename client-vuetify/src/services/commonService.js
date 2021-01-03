export default new class{

    formatDate(dateToFormat){
        return new Date(dateToFormat).toLocaleDateString(); 
    }
    formatDateTime(dateToFormat){
        let thisDate = new Date(dateToFormat);
        return thisDate.toLocaleString();  
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