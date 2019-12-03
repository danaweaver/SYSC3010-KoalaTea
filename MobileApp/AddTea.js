import React, { Component } from 'react';
import {View, StyleSheet, TextInput, Button, Text } from 'react-native';
import {sendAndWaitWithTimeout} from './socketUtil.js';

const styles = StyleSheet.create({
    mainContainer: {
      flex: 1,
      height: '100%',
      backgroundColor: 'lightyellow',
      alignContent: 'center', 
      justifyContent: 'center',
    },
    title: {
      marginLeft: 10,
      marginBottom: 50,
      fontSize: 30,
      fontWeight: 'bold'
    },
    text: {
      fontSize: 15,
      fontWeight: 'bold',
      marginLeft: 10,
    },
    textInput: {
      borderWidth: 1,
      borderColor: 'lightgrey',
      margin: 10,
      marginTop: 2,
      lineHeight: 20,
      fontSize: 15,
    }
})

export class AddTea extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      steepTime: '0',
      temp: '0',
    }
  }

  validateInputs = (name, steepTime, temp) => {
    if (name == '') {
      alert('Name can not be empty')
    } else if (!name.match(/^[\w\s]+$/)) {
      alert('No special character should be used in name')
    } else if (!steepTime.match(/^[0-9]+$/i)) {
      alert('No special character should be used in steep time')
    } else if (parseInt(steepTime) <= 0 || parseInt(steepTime) > 1800) {
      alert('Steep time is out of bound')
    } else if (!temp.match(/^[0-9]+$/i)) {
      alert('No special character should be used in temperature')
    } else if (parseInt(temp) <= 60 || parseInt(temp) > 120) {
      alert('Temperature is out of bound')
    } else {
      return true;
    }
    return false;
  }

  onSubmit = () => {
    if(this.validateInputs(this.state.name, this.state.steepTime, this.state.temp)) {
      let newTea = {
        name: this.state.name,
        steepTime: parseInt(this.state.steepTime),
        temp: parseInt(this.state.temp),
        isCustom: 1,
      }
      let newTeaProfileArray = this.props.navigation.state.params.teas
      let data = {
        "msgId": 9,
        "tea": newTea,
      }
      sendAndWaitWithTimeout(data, (msg) => {
        newTea.teaId = msg.teaId
        newTeaProfileArray.push(newTea)
        const {navigate} = this.props.navigation
        navigate('Home', {newTeaProfileArray})
      }, 9)
    }
  }

  render() {
    return (
      <View style={styles.mainContainer}> 
        <Text style={styles.title}>Add Tea</Text>
        <Text style={styles.text}>Name:</Text>
        <TextInput
          style={styles.textInput}
          placeholder="Tea name"
          onChangeText={text => this.setState({name: text})}
          value={this.state.name}
          returnKeyType="next"
          maxLength={20}
        />
        <Text style={styles.text}>Steep Time:</Text>
        <TextInput
          style={styles.textInput}
          placeholder="Steep time"
          onChangeText={text => this.setState({steepTime: text})}
          value={this.state.steepTime}
          returnKeyType="next"
          maxLength={20}
        />
        <Text style={styles.text}>Temperature:</Text>
        <TextInput
          style={styles.textInput}
          placeholder="Temperature"
          onChangeText={text => this.setState({temp: text})}
          value={this.state.temp}
          returnKeyType="done"
          maxLength={20}
        />
        <Button
            title="Save"
            onPress={() => this.onSubmit()}
        />
      </View>
    )
  }
}