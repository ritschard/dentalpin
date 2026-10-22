import type { Messages } from '@nuxt/ui'
import { defineLocale } from '@nuxt/ui/composables'

// @nuxt/ui ships no Serbian locale, so its built-in component labels
// (close buttons, calendar navigation, empty states) are defined here,
// one hand-written set per script like the app's sr-Cyrl / sr-Latn files.
export const srCyrl = defineLocale<Messages>({
  name: 'Српски (ћирилица)',
  code: 'sr-Cyrl',
  messages: {
    alert: { close: 'Затвори' },
    authForm: { hidePassword: 'Сакриј лозинку', showPassword: 'Прикажи лозинку', submit: 'Настави' },
    banner: { close: 'Затвори' },
    calendar: {
      nextMonth: 'Следећи месец',
      nextYear: 'Следећа година',
      prevMonth: 'Претходни месец',
      prevYear: 'Претходна година'
    },
    carousel: {
      dots: 'Изаберите слајд за приказ',
      goto: 'Иди на слајд {slide}',
      next: 'Следећи',
      prev: 'Претходни'
    },
    chatPrompt: { placeholder: 'Унесите поруку…' },
    chatPromptSubmit: { label: 'Пошаљи упит' },
    chatReasoning: { thinking: 'Размишља…', thought: 'Размислио', thoughtFor: 'Размишљао {duration}' },
    colorMode: {
      dark: 'Тамно',
      light: 'Светло',
      switchToDark: 'Пребаци на тамни режим',
      switchToLight: 'Пребаци на светли режим',
      system: 'Систем'
    },
    commandPalette: {
      back: 'Назад',
      close: 'Затвори',
      noData: 'Нема података',
      noMatch: 'Нема резултата',
      placeholder: 'Унесите команду или претражите…'
    },
    contentSearch: { links: 'Линкови', theme: 'Тема' },
    contentSearchButton: { label: 'Претрага…' },
    contentToc: { title: 'На овој страници' },
    dropdownMenu: { noMatch: 'Нема резултата', search: 'Претрага…' },
    dashboardSearch: { theme: 'Тема' },
    dashboardSearchButton: { label: 'Претрага…' },
    dashboardSidebarCollapse: { collapse: 'Скупи бочну траку', expand: 'Прошири бочну траку' },
    dashboardSidebarToggle: { close: 'Затвори бочну траку', open: 'Отвори бочну траку' },
    error: { clear: 'Назад на почетну' },
    fileUpload: { removeFile: 'Уклони {filename}' },
    header: { close: 'Затвори мени', open: 'Отвори мени' },
    inputMenu: { create: 'Креирај „{label}“', noData: 'Нема података', noMatch: 'Нема резултата' },
    inputNumber: { decrement: 'Смањи', increment: 'Повећај' },
    modal: { close: 'Затвори' },
    pricingTable: { caption: 'Поређење ценовних планова' },
    prose: {
      codeCollapse: { closeText: 'Скупи', name: 'код', openText: 'Прошири' },
      collapsible: { closeText: 'Сакриј', name: 'својства', openText: 'Прикажи' },
      pre: { copy: 'Копирај код у привремену меморију' }
    },
    sidebar: { close: 'Затвори', toggle: 'Пребаци' },
    selectMenu: {
      create: 'Креирај „{label}“',
      noData: 'Нема података',
      noMatch: 'Нема резултата',
      search: 'Претрага…'
    },
    slideover: { close: 'Затвори' },
    table: { noData: 'Нема података' },
    toast: { close: 'Затвори' }
  }
})

export const srLatn = defineLocale<Messages>({
  name: 'Srpski (latinica)',
  code: 'sr-Latn',
  messages: {
    alert: { close: 'Zatvori' },
    authForm: { hidePassword: 'Sakrij lozinku', showPassword: 'Prikaži lozinku', submit: 'Nastavi' },
    banner: { close: 'Zatvori' },
    calendar: {
      nextMonth: 'Sledeći mesec',
      nextYear: 'Sledeća godina',
      prevMonth: 'Prethodni mesec',
      prevYear: 'Prethodna godina'
    },
    carousel: {
      dots: 'Izaberite slajd za prikaz',
      goto: 'Idi na slajd {slide}',
      next: 'Sledeći',
      prev: 'Prethodni'
    },
    chatPrompt: { placeholder: 'Unesite poruku…' },
    chatPromptSubmit: { label: 'Pošalji upit' },
    chatReasoning: { thinking: 'Razmišlja…', thought: 'Razmislio', thoughtFor: 'Razmišljao {duration}' },
    colorMode: {
      dark: 'Tamno',
      light: 'Svetlo',
      switchToDark: 'Prebaci na tamni režim',
      switchToLight: 'Prebaci na svetli režim',
      system: 'Sistem'
    },
    commandPalette: {
      back: 'Nazad',
      close: 'Zatvori',
      noData: 'Nema podataka',
      noMatch: 'Nema rezultata',
      placeholder: 'Unesite komandu ili pretražite…'
    },
    contentSearch: { links: 'Linkovi', theme: 'Tema' },
    contentSearchButton: { label: 'Pretraga…' },
    contentToc: { title: 'Na ovoj stranici' },
    dropdownMenu: { noMatch: 'Nema rezultata', search: 'Pretraga…' },
    dashboardSearch: { theme: 'Tema' },
    dashboardSearchButton: { label: 'Pretraga…' },
    dashboardSidebarCollapse: { collapse: 'Skupi bočnu traku', expand: 'Proširi bočnu traku' },
    dashboardSidebarToggle: { close: 'Zatvori bočnu traku', open: 'Otvori bočnu traku' },
    error: { clear: 'Nazad na početnu' },
    fileUpload: { removeFile: 'Ukloni {filename}' },
    header: { close: 'Zatvori meni', open: 'Otvori meni' },
    inputMenu: { create: 'Kreiraj „{label}“', noData: 'Nema podataka', noMatch: 'Nema rezultata' },
    inputNumber: { decrement: 'Smanji', increment: 'Povećaj' },
    modal: { close: 'Zatvori' },
    pricingTable: { caption: 'Poređenje cenovnih planova' },
    prose: {
      codeCollapse: { closeText: 'Skupi', name: 'kod', openText: 'Proširi' },
      collapsible: { closeText: 'Sakrij', name: 'svojstva', openText: 'Prikaži' },
      pre: { copy: 'Kopiraj kod u privremenu memoriju' }
    },
    sidebar: { close: 'Zatvori', toggle: 'Prebaci' },
    selectMenu: {
      create: 'Kreiraj „{label}“',
      noData: 'Nema podataka',
      noMatch: 'Nema rezultata',
      search: 'Pretraga…'
    },
    slideover: { close: 'Zatvori' },
    table: { noData: 'Nema podataka' },
    toast: { close: 'Zatvori' }
  }
})
