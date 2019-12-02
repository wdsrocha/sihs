<template>
  <div>
    <div class="row">
      <div class="col-12">
        <card type="chart">
          <template slot="header">
            <div class="row">
              <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
                <h5 class="card-title">Distribuição do acesso anual ao sistema</h5>
                <!-- <h5 class="card-category">{{$t('dashboard.totalShipments')}}</h5> -->
                <h2 class="card-title">Acesso Anual</h2>
                <!-- <h2 class="card-title">{{$t('dashboard.performance')}}</h2> -->
              </div>
              <div class="col-sm-6">
                <div
                  class="btn-group btn-group-toggle"
                  :class="isRTL ? 'float-left' : 'float-right'"
                  data-toggle="buttons"
                >
                  <label
                    v-for="(option, index) in bigLineChartCategories"
                    :key="option"
                    class="btn btn-sm btn-primary btn-simple"
                    :class="{active: bigLineChart.activeIndex === index}"
                    :id="index"
                  >
                    <input
                      type="radio"
                      @click="initBigChart(index)"
                      name="options"
                      autocomplete="off"
                      :checked="bigLineChart.activeIndex === index"
                    />
                    {{option}}
                  </label>
                </div>
              </div>
            </div>
          </template>
          <div class="chart-area">
            <line-chart
              style="height: 100%"
              ref="bigChart"
              chart-id="big-line-chart"
              :chart-data="bigLineChart.chartData"
              :gradient-colors="bigLineChart.gradientColors"
              :gradient-stops="bigLineChart.gradientStops"
              :extra-options="bigLineChart.extraOptions"
            ></line-chart>
          </div>
        </card>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-4" :class="{'text-right': isRTL}">
        <card type="chart">
          <template slot="header">
            <h5 class="card-category">Percentual de acessos corretos nos 6 últimos meses</h5>
            <!-- <h5 class="card-category">{{$t('dashboard.totalShipments')}}</h5> -->
            <h3 class="card-title">
              <i class="tim-icons icon-bell-55 text-primary"></i> 90,215%
            </h3>
          </template>
          <div class="chart-area">
            <line-chart
              style="height: 100%"
              chart-id="purple-line-chart"
              :chart-data="purpleLineChart.chartData"
              :gradient-colors="purpleLineChart.gradientColors"
              :gradient-stops="purpleLineChart.gradientStops"
              :extra-options="purpleLineChart.extraOptions"
            ></line-chart>
          </div>
        </card>
      </div>
      <div class="col-lg-4" :class="{'text-right': isRTL}">
        <card type="chart">
          <template slot="header">
            <!-- <h5 class="card-category">{{$t('dashboard.dailySales')}}</h5> -->
            <h5 class="card-category">Acessos nos 6 últimos meses</h5>
            <h3 class="card-title">
              <i class="tim-icons icon-delivery-fast text-info"></i> 1000 acessos
            </h3>
          </template>
          <div class="chart-area">
            <bar-chart
              style="height: 100%"
              chart-id="blue-bar-chart"
              :chart-data="blueBarChart.chartData"
              :gradient-stops="blueBarChart.gradientStops"
              :extra-options="blueBarChart.extraOptions"
            ></bar-chart>
          </div>
        </card>
      </div>
      <div class="col-lg-4" :class="{'text-right': isRTL}">
        <card type="chart">
          <template slot="header">
            <h5 class="card-category">Percentual de acessos incorretos nos 6 últimos meses</h5>
            <!-- <h5 class="card-category">{{$t('dashboard.completedTasks')}}</h5> -->
            <h3 class="card-title">
              <i class="tim-icons icon-send text-success"></i> 09,785%
            </h3>
          </template>
          <div class="chart-area">
            <line-chart
              style="height: 100%"
              chart-id="green-line-chart"
              :chart-data="greenLineChart.chartData"
              :gradient-stops="greenLineChart.gradientStops"
              :extra-options="greenLineChart.extraOptions"
            ></line-chart>
          </div>
        </card>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <card :title="table1.title">
          <div class="table-responsive">
            <base-table :data="table1.data" :columns="table1.columns" thead-classes="text-primary"></base-table>
          </div>
        </card>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/Charts/LineChart";
import BarChart from "@/components/Charts/BarChart";
import * as chartConfigs from "@/components/Charts/config";
import TaskList from "./Dashboard/TaskList";
import UserTable from "./Dashboard/UserTable";
import config from "@/config";

import { BaseTable } from "@/components";
const tableColumns = ["Nome", "Telefone", "Acessos", "Cadastro"];
const tableData = [
  {
    id: 1,
    nome: "Dakota Rice",
    telefone: "(92) 99999-9999",
    acessos: 12,
    cadastro: "25/09/2019"
  },
  {
    id: 2,
    nome: "Minerva Hooper",
    telefone: "(92) 94444-4444",
    acessos: 10,
    cadastro: "30/01/2019"
  },
  {
    id: 3,
    nome: "Sage Rodriguez",
    telefone: "(92) 99999-9999",
    acessos: 9,
    cadastro: "25/09/2019"
  },
  {
    id: 4,
    nome: "Philip Chaney",
    telefone: "(92) 99999-9999",
    acessos: 8,
    cadastro: "25/09/2019"
  },
  {
    id: 5,
    nome: "Doris Greene",
    telefone: "(92) 99999-9999",
    acessos: 7,
    cadastro: "25/09/2019"
  },
  {
    id: 6,
    nome: "Mason Porter",
    telefone: "(92) 99999-9999",
    acessos: 5,
    cadastro: "25/09/2019"
  },
  {
    id: 7,
    nome: "Jon Porter",
    telefone: "(92) 99999-9999",
    acessos: 5,
    cadastro: "25/09/2019"
  }
];

export default {
  components: {
    LineChart,
    BarChart,
    TaskList,
    UserTable,
    BaseTable,
  },
  data() {
    return {
      table1: {
        title: "Usuários mais ativos",
        columns: [...tableColumns],
        data: [...tableData]
      },

      bigLineChart: {
        allData: [
          [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
          [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
          [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130]
        ],
        activeIndex: 0,
        chartData: null,
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: []
      },
      purpleLineChart: {
        extraOptions: chartConfigs.purpleChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [
            {
              label: "Data",
              fill: true,
              borderColor: config.colors.primary,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.primary,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.primary,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: [80, 100, 70, 80, 120, 80]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.2, 0]
      },
      greenLineChart: {
        extraOptions: chartConfigs.greenChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [
            {
              label: "My First dataset",
              fill: true,
              borderColor: config.colors.danger,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.danger,
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: config.colors.danger,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: [90, 27, 60, 12, 80, 30]
            }
          ]
        },
        gradientColors: [
          "rgba(66,134,121,0.15)",
          "rgba(66,134,121,0.0)",
          "rgba(66,134,121,0)"
        ],
        gradientStops: [1, 0.4, 0]
      },
      blueBarChart: {
        extraOptions: chartConfigs.barChartOptions,
        chartData: {
          labels: ["JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [
            {
              label: "Countries",
              fill: true,
              borderColor: config.colors.info,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: [53, 20, 10, 80, 100, 45]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      },
    };
  },
  computed: {
    enableRTL() {
      return this.$route.query.enableRTL;
    },
    isRTL() {
      return this.$rtl.isRTL;
    },
    bigLineChartCategories() {
      return this.$t("dashboard.chartCategories");
    }
  },
  methods: {
    initBigChart(index) {
      let chartData = {
        datasets: [
          {
            fill: true,
            borderColor: config.colors.primary,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: config.colors.primary,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: config.colors.primary,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: this.bigLineChart.allData[index]
          }
        ],
        labels: [
          "JAN",
          "FEB",
          "MAR",
          "APR",
          "MAY",
          "JUN",
          "JUL",
          "AUG",
          "SEP",
          "OCT",
          "NOV",
          "DEC"
        ]
      };
      this.$refs.bigChart.updateGradients(chartData);
      this.bigLineChart.chartData = chartData;
      this.bigLineChart.activeIndex = index;
    }
  },
  mounted() {
    this.i18n = this.$i18n;
    if (this.enableRTL) {
      this.i18n.locale = "ar";
      this.$rtl.enableRTL();
    }
    this.initBigChart(0);
  },
  beforeDestroy() {
    if (this.$rtl.isRTL) {
      this.i18n.locale = "en";
      this.$rtl.disableRTL();
    }
  }
};
</script>