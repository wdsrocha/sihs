<template>
  <div class="row">
    <div class="col-12">
      <card :title="table1.title">
        <div class="table-responsive">
          <base-table :data="table1.data" :columns="table1.columns" thead-classes="text-primary"></base-table>
        </div>
      </card>
    </div>
  </div>
</template>
<script>
import { BaseTable } from "@/components";
import axios from "axios";

const tableColumns = ["Nome", "Device"];
const tableData = [];

export default {
  components: {
    BaseTable
  },
  data() {
    return {
      table1: {
        title: "Usuários mais ativos",
        columns: [...tableColumns],
        data: tableData
      }
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/users")
      .then(function(response) {
        console.log(response);
        for (var i = 0; i < response.data.Users.length; i++) {
          var usr = response.data.Users[i];
          var isIn = false;
          for (var i = 0; i < tableData.length; i++) {
            if (usr.device == tableData[i].device) {
              isIn = true;
            }
          }
          if (isIn == false) {
            tableData.push({
              nome: usr.username,
              device: usr.device
            });
          }
          console.log(usr);
        }
      })
      .catch(function(error) {
        console.log(error);
      });
  }
};
</script>
<style>
</style>
