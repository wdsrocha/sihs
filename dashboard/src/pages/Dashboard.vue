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
              <i class="tim-icons icon-bell-55 text-primary"></i> {{pp}}%
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
              <i class="tim-icons icon-delivery-fast text-info"></i> {{ac}} acessos
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
              <i class="tim-icons icon-send text-success"></i> {{pn}}%
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
import axios from "axios";
import { BaseTable } from "@/components";
const tableColumns = ["Nome", "Device"];
const tableData = [];
const allData_ = [];
const positivos = [];
const negativos = [];
const total = [];
var cont = 0;
var qtd_acessos = 0;
var qtd_positivos = 0;
var qtd_negativos = 0;
var perc_p = 0;
var perc_n = 0;

export default {
  components: {
    LineChart,
    BarChart,
    TaskList,
    UserTable,
    BaseTable
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
          //console.log(usr);
        }
      })
      .catch(function(error) {
        console.log(error);
      });

    axios
      .get("http://localhost:5000/report-system-usage")
      .then(function(response) {
        console.log(response);
        var manha = response.data.morning;
        var tarde = response.data.afternoon;
        var noite = response.data.night;

        allData_.push(manha);
        allData_.push(tarde);
        allData_.push(noite);

        if (positivos.length <= 6) {
          var p = response.data.positive;
          for (var i = 0; i < p.length; i++) {
            positivos.push(p[i]);
            qtd_positivos += positivos[i];
          }
          var n = response.data.negative;
          for (var i = 0; i < n.length; i++) {
            negativos.push(n[i]);
            qtd_negativos += negativos[i];
          }
          for (var i = 0; i < 6; i++) {
            //total.push(manha[i] + tarde[i] + noite[i]);
            total.push(positivos[i]+negativos[i])
            qtd_acessos += total[i];
          }
          perc_p = (qtd_positivos/qtd_acessos)*100.0;
          perc_n = (qtd_negativos/qtd_acessos)*100.0;
        }
        console.log("positivos=", positivos);
        console.log("negativos=", negativos);
        console.log("total=", total);
        //console.log("aqui tem o alldata", allData_);
      })
      .catch(function(error) {
        console.log(error);
      });

    this.i18n = this.$i18n;
    if (this.enableRTL) {
      this.i18n.locale = "ar";
      this.$rtl.enableRTL();
    }
    this.initBigChart(0);
  },

  getusers() {},

  data() {
    return {
      table1: {
        title: "Usuários mais ativos",
        columns: [...tableColumns],
        data: tableData
      },

      pp: perc_p,
      pn: perc_n,
      ac: qtd_acessos,

      bigLineChart: {
        allData: allData_,
        // allData: [
        //   [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
        //   [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
        //   [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130]
        // ],
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
              label: "Acertos",
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
              data: positivos //[80, 100, 70, 80, 120, 80]
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
              label: "Erros",
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
              data: negativos //[90, 27, 60, 12, 80, 30]
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
              label: "Acessos",
              fill: true,
              borderColor: config.colors.info,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: total //[53, 20, 10, 80, 100, 45]
            }
          ]
        },
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0]
      }
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
  beforeDestroy() {
    if (this.$rtl.isRTL) {
      this.i18n.locale = "en";
      this.$rtl.disableRTL();
    }
  }
};
</script>