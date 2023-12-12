## 接口的有关问题

### analysisList.vue

### medicineList.vue

```vue
  async function sendPatient() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/sendPatient/', {
          name: patient[0].name, id: patient[0].id
        });
    } catch (error) {
        console.error('Error fetching patient:', error);
    }
  }

  async function sendDoctor() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/sendDoctor/', {
          username: username
        });
    } catch (error) {
        console.error('Error sending doctor:', error);
    }
  }
  sendDoctor()
```

这个函数是用来干什么的？

```vue
  async function sendMedicineGroup() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/sendMedicineList/', {
          medicineGroup: medicineGroup
        });
    } catch (error) {
        console.error('Error sending medicineList:', error);
    }
    sendPatient();
  }
```

这个函数应该同时传入病人的id或者username，以及医生的username

### addDoctor.vue

```vue
  async function addDoctor() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/addDoctor/', {
          newDoctor: authors[0]
        });
    } catch (error) {
        console.error('Error adding doctor:', error);
    }
  }
```

应该传入用户名，密码等信息，信息是不是太少了

### addPatient.vue

```vue
  async function addPatient() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/addPatient/', {
          newDoctor: authors[0]
        });
    } catch (error) {
        console.error('Error adding patient:', error);
    }
  }

```

同上