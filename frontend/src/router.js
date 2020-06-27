import Vue from 'vue';
import VueRouter from 'vue-router';
import VueMeta from 'vue-meta';

import HomePage from './views/HomePage.vue';
import QuestionPage from './views/QuestionPage.vue';
import QuestionListPage from './views/QuestionListPage.vue';
import QuestionDetailPage from './views/QuestionDetailPage.vue';
import CategoryListPage from './views/CategoryListPage.vue';
import CategoryDetailPage from './views/CategoryDetailPage.vue';
import TagListPage from './views/TagListPage.vue';
import TagDetailPage from './views/TagDetailPage.vue';
import AuthorListPage from './views/AuthorListPage.vue';
import AuthorDetailPage from './views/AuthorDetailPage.vue';
import QuizListPage from './views/QuizListPage.vue';
import QuizDetailPage from './views/QuizDetailPage.vue';
import AboutPage from './views/AboutPage.vue';
import StatsPage from './views/StatsPage.vue';
import GlossaryPage from './views/GlossaryPage.vue';
import ContributePage from './views/ContributePage.vue';
import NotFoundPage from './views/NotFoundPage.vue';

Vue.use(VueRouter);
Vue.use(VueMeta);

const routes = [
  {
    path: '/', name: 'home', component: HomePage,
  },
  {
    path: '/questions',
    component: QuestionPage,
    children: [
      {
        path: '',
        name: 'question-list',
        component: QuestionListPage,
      },
      {
        path: ':questionId',
        name: 'question-detail',
        component: QuestionDetailPage,
      },
    ],
  },
  {
    path: '/categories',
    name: 'category-list',
    component: CategoryListPage,
  },
  {
    path: '/categories/:categoryName',
    name: 'category-detail',
    component: CategoryDetailPage,
  },
  {
    path: '/tags',
    name: 'tag-list',
    component: TagListPage,
  },
  {
    path: '/tags/:tagName',
    name: 'tag-detail',
    component: TagDetailPage,
  },
  {
    path: '/auteurs',
    name: 'author-list',
    component: AuthorListPage,
  },
  {
    path: '/auteurs/:authorName',
    name: 'author-detail',
    component: AuthorDetailPage,
  },
  {
    path: '/quiz',
    name: 'quiz-list',
    component: QuizListPage,
  },
  {
    path: '/quiz/:quizId',
    name: 'quiz-detail',
    component: QuizDetailPage,
  },
  {
    path: '/a-propos',
    name: 'about',
    component: AboutPage,
  },
  {
    path: '/stats',
    name: 'stats',
    component: StatsPage,
  },
  {
    path: '/glossaire',
    name: 'glossary',
    component: GlossaryPage,
  },
  {
    path: '/contribuer',
    name: 'contribute',
    component: ContributePage,
  },
  {
    // will match everything
    path: '*',
    name: '404',
    component: NotFoundPage,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
