<template>
    <div class="row">
      <div class="col-12">
        <card :title="table1.title">
          <div class="table-responsive">
            <base-table :data="table1.data"
                        :columns="table1.columns"
                        thead-classes="text-primary">
            </base-table>
          </div>
        </card>
      </div>
    </div>
</template>
<script>
import { BaseTable } from "@/components";
const tableColumns = ["Nome", "Device", "Acessos", "Cadastro"];
const tableData = [
  {
    id: 1,
    nome: "Dakota Rice",
    device: "12345",
    acessos: 12,
    cadastro: "25/09/2019"
  },
  {
    id: 2,
    nome: "Minerva Hooper",
    device: "12345",
    acessos: 10,
    cadastro: "30/01/2019"
  },
  {
    id: 3,
    nome: "Sage Rodriguez",
    device: "12345",
    acessos: 9,
    cadastro: "25/09/2019"
  },
  {
    id: 4,
    nome: "Philip Chaney",
    device: "12345",
    acessos: 8,
    cadastro: "25/09/2019"
  },
  {
    id: 5,
    nome: "Doris Greene",
    device: "12345",
    acessos: 7,
    cadastro: "25/09/2019"
  },
  {
    id: 6,
    nome: "Mason Porter",
    device: "12345",
    acessos: 5,
    cadastro: "25/09/2019"
  },
  {
    id: 7,
    nome: "Jon Porter",
    device: "12345",
    acessos: 5,
    cadastro: "25/09/2019"
  }
];

export default {
  components: {
    BaseTable
  },
  data() {
    return {
      table1: {
        title: "Simple Table",
        columns: [...tableColumns],
        data: [...tableData]
      },
      table2: {
        title: "Table on Plain Background",
        columns: [...tableColumns],
        data: [...tableData]
      }
    };
  }
};
</script>
<style>
</style>
