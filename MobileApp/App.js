import {createAppContainer} from 'react-navigation';
import {createStackNavigator} from 'react-navigation-stack';
import {LoadScreen} from './LoadScreen.js';
import {HomeScreen} from './HomeScreen.js';
import {AddTea} from './AddTea.js'

const MainNavigator = createStackNavigator({
  Load: {
    screen: LoadScreen,
    navigationOptions: () => ({
      headerShown: false,
    }),
    params: {isBrewing: false}
  },
  Home: {
    screen: HomeScreen,
    navigationOptions: () => ({
      title: 'Home Screen',
      headerLeft: null,
    })
  },
  AddTea: {
    screen: AddTea,
    navigationOptions: () => ({
      title: 'Add Tea'
    })
  }
});

const App = createAppContainer(MainNavigator);

export default App;
