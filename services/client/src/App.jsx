import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import axios from 'axios';


import UserList from './components/UsersList';
import AddUser from './components/AddUser';
import About from './components/About';
import NavBar from './components/NavBar';
import Form from './components/Form';
import Logout from './components/Logout';


class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
      title: 'TestDriven.io',
      formData: {
        username: '',
        email: '',
        password: ''
      },
      isAuthenticated: false
    };
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then((res) => {
        this.setState({ users: res.data.data.users });
      })
      .catch((err) => {
        console.log(err);
      });
  }

  addUser(event) {
    event.preventDefault();
    // console.log('sanity check!');
    // console.log(this.state);
    const { username, email } = this.state;

    const data = { username, email };
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then((res) => {
        this.getUsers();
        this.setState({ username: '', email: '' });
      })
      .catch((err) => {
        console.log(err);
      });
  }

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }

  handleFormChange(event) {
    const { formData } = this.state;
    formData[event.target.name] = event.target.value;
    this.setState(formData);
  }

  handleUserFormSubmit(event) {
    event.preventDefault();
    const { formData } = this.state;
    const { email, password, username } = formData;
    const formType = window.location.href.split('/').reverse()[0];
    const data = { email, password };
    if (formType === 'register') {
      data.username = username;
    }
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;
    axios.post(url, data)
      .then((res) => {
        this.setState({
          formData: { username: '', email: '', password: '' },
          username: '',
          email: '',
          isAuthenticated: true
        });
        window.localStorage.setItem('authToken', res.data.auth_token);
        this.getUsers();
      })
      .catch((err) => {
        console.log(err);
      });
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
  }

  render() {
    const {
      title, username, email, users, formData, isAuthenticated
    } = this.state;
    return (
      <div>
        <NavBar title={title} />
        <div className="container">
          <div className="row">
            <div className="col-md-4">
              <br />
              <Switch>
                <Route
                  exact
                  path="/"
                  render={() => (
                    <div>
                      <h1>All Users</h1>
                      <hr />
                      <br />
                      <AddUser
                        username={username}
                        email={email}
                        handleChange={this.handleChange}
                        addUser={this.addUser}
                      />
                      <br />
                      <UserList users={users} />
                    </div>
                  )}
                />
                <Route
                  exact
                  path="/about"
                  component={About}
                />
                <Route
                  exact
                  path="/register"
                  render={() => (
                    <Form
                      formType="Register"
                      formData={formData}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      handleFormChange={this.handleFormChange}
                      isAuthenticated={isAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/login"
                  render={() => (
                    <Form
                      formType="Login"
                      formData={formData}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      handleFormChange={this.handleFormChange}
                      isAuthenticated={isAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/logout"
                  render={() => (
                    <Logout
                      logoutUser={this.logoutUser}
                      isAuthenticated={isAuthenticated}
                    />
                  )}
                />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// App.propTypes = {
//   isAuthenticated: PropTypes.string.isRequired,
// }

export default App;
