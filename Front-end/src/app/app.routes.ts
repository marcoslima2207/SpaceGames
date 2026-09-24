import { Routes } from '@angular/router';
import { AccountPageComponent } from './account-page.component';
import { AuthPageComponent } from './auth-page.component';
import { GameDetailComponent } from './game-detail.component';
import { HomeComponent } from './home.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: AuthPageComponent, data: { mode: 'login' } },
  { path: 'cadastro', component: AuthPageComponent, data: { mode: 'register' } },
  { path: 'jogo/:id', component: GameDetailComponent },
  { path: 'pesquisa', component: HomeComponent },
  { path: 'favoritos', component: AccountPageComponent, data: { mode: 'favoritos' } },
  { path: 'carrinho', component: AccountPageComponent, data: { mode: 'carrinho' } },
  { path: 'biblioteca', component: AccountPageComponent, data: { mode: 'biblioteca' } },
  { path: 'perfil', component: AccountPageComponent, data: { mode: 'perfil' } },
  { path: '**', redirectTo: '' }
];