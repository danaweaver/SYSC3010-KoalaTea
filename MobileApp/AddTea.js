import React, { Component } from 'react';
import {View, StyleSheet, TextInput, Button, Alert } from 'react-native';

const styles = StyleSheet.create({
    mainContainer: {
      flex: 1,
      height: '100%',
      backgroundColor: 'lightyellow',
    },
})

export class AddTea extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      steepTime: '0',
      temp: '0',
    };
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
        steepTime: this.state.steepTime,
        temp: this.state.temp
      }
      let newTeaProfileArray = this.props.navigation.state.params.teas
      newTeaProfileArray.push(newTea)
      const {navigate} = this.props.navigation
      navigate('Home', {teas: newTeaProfileArray})
    } else {
      // Alert.alert(
      //   'Alert Title',
      //   'My Alert Msg',
      //   [
      //     {text: 'Ask me later', onPress: () => console.log('Ask me later pressed')},
      //     {
      //       text: 'Cancel',
      //       onPress: () => console.log('Cancel Pressed'),
      //       style: 'cancel',
      //     },
      //     {text: 'OK', onPress: () => console.log('OK Pressed')},
      //   ],
      //   {cancelable: false},
      // );
    }
  }

  render() {
    return (
      <View style={styles.mainContainer}> 
        <TextInput
          style={styles.textInput}
          placeholder="Tea name"
          onChangeText={text => this.setState({name: text})}
          value={this.state.name}
          returnKeyType="next"
          maxLength={20}
        />
        <TextInput
          style={styles.textInput}
          placeholder="Steep time"
          onChangeText={text => this.setState({steepTime: text})}
          value={this.state.steepTime}
          returnKeyType="next"
          maxLength={20}
        />
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